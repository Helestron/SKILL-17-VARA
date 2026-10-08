#!/usr/bin/env python3
"""Testes de ponta a ponta dos scripts da skill (sem rede e sem o Helestron instalado).

Uso: python3 testes/testar.py   (requer reportlab e pdfplumber ou pypdf para a pasta sintética)
"""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SK = RAIZ / "skill-17a-lote-minutas-helestron"
S = SK / "scripts"
PY = sys.executable
falhas = []


def rodar(*args, esperado=0):
    r = subprocess.run([PY, "-I", *map(str, args)], capture_output=True, text=True, encoding="utf-8")
    if esperado is not None and r.returncode != esperado:
        falhas.append(f"{' '.join(map(str, args[:3]))}: código {r.returncode} (esperado {esperado})\n{r.stdout[-800:]}{r.stderr[-800:]}")
    return r


def checar(cond, msg):
    if not cond:
        falhas.append(msg)


def minuta(tmp: Path, nome: str, texto: str) -> Path:
    p = tmp / nome
    p.write_text(texto, encoding="utf-8")
    return p


def main():
    tmp = Path(tempfile.mkdtemp(prefix="vara17_"))
    try:
        # 1. pasta sintética do Helestron, inventário, texto, transcrições e sigilo
        n = json.loads(subprocess.run([PY, "-I", RAIZ / "testes" / "criar_fixture.py", tmp / "acervo", S],
                                      capture_output=True, text=True, check=True).stdout)
        r = rodar(S / "autos.py", "inventario", tmp / "acervo", "--lista", n["n1"][:15], n["n2"], n["n3"], "0000001-00.2024.8.02.0001")
        checar("TRABALHO=" in r.stdout and "inválidos" in r.stdout and "(processo sigiloso)" in r.stdout, "inventário")
        checar(n["n3"] not in r.stdout, "número do sigiloso exposto no inventário")
        t = r.stdout.split("TRABALHO=")[1].splitlines()[0].strip()
        r = rodar(S / "autos.py", "preparar", "-t", t)
        checar("1 transcrição" in r.stdout and "Mandado de Segurança" in r.stdout, "preparar")
        r = rodar(S / "autos.py", "ler", "1", "--fls", "4-4", "-t", t)
        checar("[fl. 4]" in r.stdout and "CONTESTACAO" in r.stdout, "ler por folhas")
        r = rodar(S / "autos.py", "transcricoes", "1", "--ler", "1", "-t", t)
        checar("[12:30] Testemunha" in r.stdout and "2024-05-10" in r.stdout, "transcrição .srt")
        rodar(S / "autos.py", "ler", "3", "--fls", "1-1", "-t", t, esperado=1)  # sigiloso sem autorização
        rodar(S / "autos.py", "autorizar", "3", "--ordem", "autorizo o sigiloso", "-t", t)
        rodar(S / "autos.py", "preparar", "3", "-t", t)
        r = rodar(S / "autos.py", "ler", "3", "--fls", "1-1", "-t", t)
        checar("SEGREDO" in r.stdout, "sigiloso autorizado")
        r = rodar(S / "autos.py", "inventario", tmp / "acervo", "--lista", n["n1"], n["n2"], n["n3"])
        checar("lote01" in r.stdout, "a mesma lista deve retomar o lote aberto")

        # 2. portão
        exemplo = RAIZ / "testes" / "minuta_exemplo_sentenca.txt"
        r = rodar(S / "verificar_minuta.py", exemplo)
        checar(json.loads(r.stdout)["resultado"] == "OK", "exemplo deveria passar no portão")
        base = exemplo.read_text(encoding="utf-8")
        ruins = {
            "numerada": base.replace("Réplica às fls. 70/75.", "5. Réplica às fls. 70/75."),
            "primeira_pessoa": base.replace("Com efeito, o autor", "Entendo que o autor"),
            "vedado": base.replace("Com efeito,", "Compulsando os autos,"),
            "sem_pri": base.replace("P. R. I.", "Publique-se."),
            "titulo": base.replace("É o Relatório.\n", "É o Relatório.\nDa preliminar\n"),
            "metodo": base.replace("Com efeito,", "Feita a leitura integral dos autos,"),
            "desbalanceada": base.replace("**coisa julgada**", "**coisa julgada"),
        }
        for nome, txt in ruins.items():
            r = rodar(S / "verificar_minuta.py", minuta(tmp, f"{nome}.txt", txt), esperado=1)
            checar(json.loads(r.stdout)["resultado"] == "BLOQUEADO", f"portão deveria bloquear: {nome}")

        # 3. geração do Word
        saida = tmp / "minutas"
        r = rodar(S / "gerar_minuta.py", exemplo, "--saida", saida)
        res = json.loads(r.stdout)
        checar(res["resultado"] == "OK", "geração")
        limpa, anot = Path(res["limpa"]), Path(res["anotada"])
        xl = zipfile.ZipFile(limpa).read("word/document.xml").decode()
        xa = zipfile.ZipFile(anot).read("word/document.xml").decode()
        checar("FF0000" not in xl and "Conferir" not in xl and "<w:numPr>" not in xl, "limpa sem vermelho/numeração")
        checar("FF0000" in xa and "Conferir" in xa and "Resolução CNJ" in xa, "anotada com vermelho e ressalva")
        checar("Courier New" in xl and 'w:ind w:left="2268"' in xl and 'w:firstLine="1417"' in xl, "formatação dos modelos")
        rodar(S / "gerar_minuta.py", minuta(tmp, "bloq.txt", ruins["numerada"]), "--saida", saida, esperado=1)
        checar(not (saida / "bloq.docx").exists(), "minuta bloqueada não pode gerar .docx")

        # 4. ledger
        r = rodar(S / "ledger.py", "conferir", minuta(tmp, "cit.txt", base.replace("(art. 373, I, do CPC)", "(art. 373, I, do CPC; REsp n.º 1.340.553/RS)")), "-t", t, esperado=1)
        checar("REsp n.º 1.340.553" in r.stdout, "precedente sem ledger deve bloquear")
        e = [{"tipo": "precedente", "chave": "REsp n.º 1.340.553", "tribunal": "STJ", "orgao": "Primeira Seção", "relator": "Min. X",
              "julgamento": "2018-09-12", "fonte": "https://scon.stj.jus.br/x", "status": "VERIFIED", "aderencia": "teste",
              "trecho_literal": "RECURSO ESPECIAL REPETITIVO. PRESCRIÇÃO INTERCORRENTE. ART. 40 DA LEF."},
             {"tipo": "precedente", "chave": "IRDR n.º 3", "tribunal": "TJAL", "orgao": "Seção Especializada Cível",
              "relator": "Des. Y", "julgamento": "2025-07-08", "fonte": "https://www2.tjal.jus.br/cjsg/x", "status": "VERIFIED",
              "aderencia": "teste", "trecho_literal": "1.1. O mero cumprimento do interstício temporal no posto não implica preterição."}]
        (tmp / "e.json").write_text(json.dumps(e), encoding="utf-8")
        rodar(S / "ledger.py", "add", tmp / "e.json", "-t", t)
        rodar(S / "ledger.py", "conferir", tmp / "cit.txt", "-t", t, esperado=0)
        e[0]["fonte"] = "https://blog.exemplo.com/x"
        (tmp / "e2.json").write_text(json.dumps(e), encoding="utf-8")
        rodar(S / "ledger.py", "add", tmp / "e2.json", "-t", t, esperado=1)
        rodar(S / "ledger.py", "calc", tmp / "c.json", "add", "--descricao", "x", "--expr", "__import__('os')", esperado=1)

        # 5. modelos
        for m in sorted((SK / "modelos").glob("*.txt")):
            txt = m.read_text(encoding="utf-8")
            checar(txt.splitlines()[1].startswith("@ato "), f"modelo sem @ato: {m.name}")
        r = rodar(S / "importar_modelo.py", "buscar", "promoção militar inativo")
        checar("inativo" in r.stdout, "busca de modelos")
        if shutil.which("soffice"):
            r = rodar(S / "importar_modelo.py", next((SK / "modelos" / "originais").glob("*0750345*")))
            checar("@ato sentença" in r.stdout and "!! Desse modo, determino a exclusão" in r.stdout, "importação de RTF")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if falhas:
        print("FALHAS:\n- " + "\n- ".join(falhas))
        return 1
    print("todos os testes passaram")
    return 0


if __name__ == "__main__":
    sys.exit(main())
