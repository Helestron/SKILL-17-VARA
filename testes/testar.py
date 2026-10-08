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


def subst(texto: str, a: str, b: str) -> str:
    assert a in texto, f"trecho ausente no texto-base do teste: {a!r}"
    return texto.replace(a, b)


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

        # 1-b. transcrições em .vtt e .docx (formatos alternativos do aplicativo)
        tr = tmp / "Transcrições"
        (tr / f"{n['n2']}_audiencia_15-03-2024.vtt").write_text(
            "WEBVTT\n\n00:01:05.000 --> 00:01:09.000\nJuiz: Ouvida a testemunha.\n", encoding="utf-8")
        with zipfile.ZipFile(tr / f"Termo {n['n2']}.docx", "w") as z:
            z.writestr("word/document.xml", '<w:document xmlns:w="x"><w:body><w:p><w:r><w:t>Depoimento: o fiscal reteve a carga.</w:t></w:r></w:p></w:body></w:document>')
        r = rodar(S / "ponte_helestron.py", "transcricoes", "--transcricoes", tr, "--numero", n["n2"])
        idx = json.loads(r.stdout)["indice"][n["n2"]]
        checar(len(idx) == 2 and idx[0]["data"] == "2024-03-15", "índice de transcrições .vtt/.docx")
        r = rodar(S / "ponte_helestron.py", "ler-transcricao", next(x["arquivo"] for x in idx if x["tipo"] == "vtt"))
        checar("[01:05] Juiz: Ouvida a testemunha." in r.stdout, "leitura de .vtt")
        r = rodar(S / "ponte_helestron.py", "ler-transcricao", next(x["arquivo"] for x in idx if x["tipo"] == "docx"))
        checar("o fiscal reteve a carga" in r.stdout, "leitura de .docx")

        # 2. portão
        exemplo = RAIZ / "testes" / "minuta_exemplo_sentenca.txt"
        r = rodar(S / "verificar_minuta.py", exemplo)
        checar(json.loads(r.stdout)["resultado"] == "OK", "exemplo deveria passar no portão")
        base = exemplo.read_text(encoding="utf-8")
        ruins = {
            "numerada": subst(base, "Réplica às fls. 70/75.", "5. Réplica às fls. 70/75."),
            "primeira_pessoa": subst(base, "Com efeito, o autor", "Entendo que o autor"),
            "vedado": subst(base, "Com efeito,", "Compulsando os autos,"),
            "sem_pri": subst(base, "P. R. I.", "Publique-se."),
            "titulo": subst(base, "É o Relatório.\n", "É o Relatório.\nDa preliminar\n"),
            "metodo": subst(base, "Com efeito,", "Feita a leitura integral dos autos,"),
            "desbalanceada": subst(base, "**coisa julgada**", "**coisa julgada"),
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
        r = rodar(S / "ledger.py", "conferir", minuta(tmp, "cit.txt", subst(base, "(art. 373, I, do CPC)", "(art. 373, I, do CPC; REsp n.º 1.340.553/RS)")), "-t", t, esperado=1)
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

        # 6. regressões da revisão adversarial
        r = rodar(S / "verificar_minuta.py", minuta(tmp, "afl.txt", subst(base, "Réplica às fls. 70/75.", "Réplica às fls. 70/75, com documento juntado à fl. 76.")))
        checar(json.loads(r.stdout)["resultado"] == "OK", "'à fl.' é a forma correta e não pode bloquear")
        r = rodar(S / "verificar_minuta.py", minuta(tmp, "semproc.txt", subst(base, "@processo 0714346-41.2024.8.02.0001\n", "")), esperado=1)
        checar("@processo" in r.stdout, "@processo obrigatório")
        desp = ("@ato despacho\n@processo 0714346-41.2024.8.02.0001\nDefiro a produção de prova documental requerida às fls. 80/81.\n"
                "Intime-se o Estado de Alagoas para juntar a ficha funcional do autor no prazo de 15 (quinze) dias.\n"
                "Decorrido o prazo, voltem conclusos para sentença.\nCumpra-se.\n")
        r = rodar(S / "verificar_minuta.py", minuta(tmp, "desp.txt", desp))
        checar(json.loads(r.stdout)["resultado"] == "OK", "despacho com 1ª pessoa deve passar")
        r = rodar(S / "gerar_minuta.py", tmp / "desp.txt", "--saida", saida)
        xd = zipfile.ZipFile(json.loads(r.stdout)["limpa"]).read("word/document.xml").decode()
        checar(xd.count('<w:u w:val="single"/>') >= 2, "comandos do despacho sublinhados")
        homol = subst(base, "Diante do exposto, julgo improcedente a demanda.", "Diante do exposto, homologo o acordo de fls. 90/92.")
        r = rodar(S / "verificar_minuta.py", minuta(tmp, "homol.txt", homol))
        checar(json.loads(r.stdout)["resultado"] == "OK", "sentença homologatória deve passar")
        r = rodar(S / "ledger.py", "calc", tmp / "c2.json", "add", "--descricao", "razão", "--expr", "round(4.908,00 / 1.412,00, 2)")
        checar('"resultado": 3.48' in r.stdout, "cálculo com decimal brasileiro e round(x, 2)")
        r = rodar(S / "autos.py", "inventario", tmp / "acervo", "--lista", n["n1"], "-t", tmp / "outro_trab")
        checar("outro_trab" in r.stdout and "inválidos" not in r.stdout, "-t depois de --lista")
        r = rodar(S / "autos.py", "marcar", "1", "minutado", "--justificativa", "gerúndio mantido: citação", "-t", tmp / "outro_trab")
        r = rodar(S / "autos.py", "marcar", "1", "minutado", "--justificativa", "dois-pontos mantido: bloco", "-t", tmp / "outro_trab")
        est = json.loads((tmp / "outro_trab" / "estado.json").read_text(encoding="utf-8"))
        checar("gerúndio" in est["processos"][n["n1"]]["justificativa"] and "dois-pontos" in est["processos"][n["n1"]]["justificativa"],
               "justificativas acumuladas")
        verm = subst(base, "Diante do exposto, julgo improcedente a demanda.",
                            "Diante do exposto, julgo {{Conferir: pedido subsidiário}} improcedente a demanda.")
        r = rodar(S / "gerar_minuta.py", minuta(tmp, "verm.txt", subst(verm, "@processo 0714346-41.2024.8.02.0001", "@processo 0750345-89.2023.8.02.0001")), "--saida", saida)
        res = json.loads(r.stdout)
        checar(res["resultado"] == "OK", "apontamento no início do dispositivo não pode reprovar a limpa")
        xv = zipfile.ZipFile(res["limpa"]).read("word/document.xml").decode()
        texto_v = "".join(__import__("re").findall(r"<w:t[^>]*>([^<]*)</w:t>", xv))
        checar("julgo improcedente" in texto_v and "  " not in texto_v, "limpa sem espaço duplo")
        serie = subst(base, "> 1.1. O mero", "> Apelação Cível n.º 0702075-63.2025.8.02.0001, Rel. Des. A, julgado em 12/08/2026.\n"
                             "> Apelação Cível n.º 0726628-14.2024.8.02.0001, Rel. Des. A, julgado em 12/08/2026.\n"
                             "> Apelação Cível n.º 0739309-84.2022.8.02.0001, Rel. Des. B, julgado em 05/08/2026.\n> 1.1. O mero")
        r = rodar(S / "verificar_minuta.py", minuta(tmp, "serie.txt", serie))
        checar("precedentes em série" in r.stdout, "precedentes em série")
        # Helestron simulado: sigilosos fora do acervo, pelo `caminhos --json`
        fora = tmp / "SigilososFora" / "Lote X"
        fora.mkdir(parents=True)
        shutil.copy(next((tmp / "acervo").glob(f"{n['n2']}.pdf")), fora / "0700099-55.2024.8.02.0001.pdf")
        falso = tmp / "helestron_falso"
        falso.write_text("#!/bin/sh\necho '{\"versao\": \"1.0.9\", \"acervo\": \"" + str(tmp / "acervo") + "\", \"sigilosos\": \""
                         + str(tmp / "SigilososFora") + "\"}'\n", encoding="utf-8")
        falso.chmod(0o755)
        env = dict(__import__("os").environ, HELESTRON_PYTHON=str(falso))
        r = subprocess.run([PY, "-I", str(S / "autos.py"), "inventario", "-t", str(tmp / "trab_sig")], capture_output=True,
                           text=True, encoding="utf-8", env=env)
        checar("0700099-55.2024" not in r.stdout and r.stdout.count("(processo sigiloso)") >= 2,
               "sigiloso fora do acervo deve entrar no inventário, sem expor o número")
        # PDF de outra origem com carimbo "fls. 100": a folha é a carimbada
        from reportlab.pdfgen import canvas
        outra = tmp / "outra"; outra.mkdir()
        c = canvas.Canvas(str(outra / "0700100-40.2024.8.02.0001.pdf"))
        for k in range(3):
            c.drawString(500, 810, f"fls. {100 + k}"); c.drawString(60, 780, f"Peça de outra origem, página {k + 1}"); c.showPage()
        c.save()
        r = rodar(S / "autos.py", "inventario", outra, "-t", tmp / "trab_outra")
        rodar(S / "autos.py", "preparar", "-t", tmp / "trab_outra")
        r = rodar(S / "autos.py", "ler", "1", "--fls", "101-101", "-t", tmp / "trab_outra")
        checar("[fl. 101]" in r.stdout and "página 2" in r.stdout, "folha carimbada prevalece sobre a posição no PDF")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if falhas:
        print("FALHAS:\n- " + "\n- ".join(falhas))
        return 1
    print("todos os testes passaram")
    return 0


if __name__ == "__main__":
    sys.exit(main())
