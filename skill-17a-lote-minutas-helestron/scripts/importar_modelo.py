#!/usr/bin/env python3
"""Converte um modelo da vara (.docx; .rtf, .odt ou .doc por conversão) para a marcação da minuta.

Uso:
  python -I importar_modelo.py <modelo> [--saida <arquivo.txt>]
  python -I importar_modelo.py buscar "<termos>" [--max 8]

O primeiro uso preserva negrito, sublinhado e itálico, reconhece as transcrições (Courier ou recuo
esquerdo) e os parágrafos decisórios em negrito e sublinhado ('!! '), descarta a numeração automática
e põe cabeçalho e assinatura (que vêm do modelo do SAJ) como comentário ('// '). Serve para ampliar a
biblioteca de `modelos/` e para ler os modelos próprios do usuário.
O segundo ordena os modelos (os da skill e os de `pastas.modelos_usuario`) pela semelhança do nome
e do início do texto com os termos dados — é assim que se acha o modelo de tema mais próximo.

Conversão de .rtf/.odt/.doc: LibreOffice (`soffice`), se houver; no Windows, o Word instalado.
"""
import json
import os
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
RAIZ = Path(__file__).resolve().parent.parent


def _converter(arq: Path, destino: Path) -> Path:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        # sem as variáveis de localidade: o RTF com \fcharset1 ("padrão do sistema") seria lido como UTF-8
        # quando o Python repassa LC_CTYPE=C.UTF-8, e os acentos se perderiam
        env = {k: v for k, v in os.environ.items() if not k.startswith("LC_") and k != "LANG"}
        subprocess.run([soffice, "--headless", "--convert-to", "docx", "--outdir", str(destino), str(arq)],
                       capture_output=True, timeout=180, env=env)
        out = destino / (arq.stem + ".docx")
        if out.exists():
            return out
    if os.name == "nt":
        out = destino / (arq.stem + ".docx")
        ps = ("$w = New-Object -ComObject Word.Application; $w.Visible = $false; "
              f"$d = $w.Documents.Open('{arq}', $false, $true); $d.SaveAs2('{out}', 16); $d.Close($false); $w.Quit()")
        subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, timeout=180)
        if out.exists():
            return out
    raise RuntimeError(f"não foi possível converter {arq.name} para .docx (instale o LibreOffice ou use o Word)")


def _ligado(el, tag):
    x = el.find(W + tag) if el is not None else None
    if x is None:
        return False
    val = x.get(W + "val")
    return val not in ("false", "0", "none")


def _paragrafos(docx: Path):
    with zipfile.ZipFile(docx) as z:
        raiz = ET.fromstring(z.read("word/document.xml"))
    for p in raiz.iter(W + "p"):
        ppr = p.find(W + "pPr")
        ind = ppr.find(W + "ind") if ppr is not None else None
        recuo = 0
        if ind is not None:
            for chave in ("left", "start"):
                v = ind.get(W + chave)
                if v and v.lstrip("-").isdigit():
                    recuo = max(recuo, int(v))
        runs = []
        for r in p.iter(W + "r"):
            rpr = r.find(W + "rPr")
            fonte = ""
            if rpr is not None and rpr.find(W + "rFonts") is not None:
                fonte = rpr.find(W + "rFonts").get(W + "ascii") or ""
            texto = ""
            for filho in r:
                if filho.tag == W + "t":
                    texto += filho.text or ""
                elif filho.tag in (W + "tab", W + "br"):
                    texto += " "
            if texto:
                runs.append({"t": texto, "b": _ligado(rpr, "b"), "i": _ligado(rpr, "i"), "u": _ligado(rpr, "u"),
                             "courier": "courier" in fonte.lower()})
        texto = "".join(r["t"] for r in runs).strip()
        if texto:
            yield {"texto": texto, "runs": runs, "recuo": recuo}


def _inline(runs, tirar=()):
    """Trechos com formatação → marcação, com pilha (fecha na ordem inversa da abertura, sem cruzar
    marcas) e com os espaços das bordas fora das marcas."""
    marcas = {"b": "**", "u": "__", "i": "*"}
    out, pilha = [], []

    def fechar_ate(k):
        reabrir = []
        while pilha:
            topo = pilha.pop()
            out.append("\x01" + marcas[topo])
            if topo == k:
                break
            reabrir.append(topo)
        for x in reversed(reabrir):
            out.append(marcas[x])
            pilha.append(x)

    for r in runs:
        t = r["t"].replace("*", "\\*")
        if not t.strip():
            out.append(t)
            continue
        quer = {k for k in "bui" if r[k] and k not in tirar}
        inicio, miolo, fim = re.match(r"^(\s*)(.*?)(\s*)$", t, re.S).groups()
        for k in [x for x in reversed(pilha) if x not in quer]:
            fechar_ate(k)
        out.append(inicio)
        for k in "bui":
            if k in quer and k not in pilha:
                out.append(marcas[k])
                pilha.append(k)
        out.append(miolo)
        out.append("\x00" + fim)  # espaço final: decide-se no próximo trecho
    while pilha:
        out.append("\x01" + marcas[pilha.pop()])
    s = "".join(out)
    # marca de fechamento logo depois de espaço volta para antes dele ("texto** " e não "texto **")
    s = re.sub(r"\x00(\s*)((?:\x01(?:\*\*|__|\*))+)", r"\2\1", s).replace("\x00", "").replace("\x01", "")
    return re.sub(r"\s{2,}", " ", s).strip()


def importar(arq: Path) -> str:
    with tempfile.TemporaryDirectory() as tmp:
        docx = arq if arq.suffix.lower() == ".docx" else _converter(arq, Path(tmp))
        pars = list(_paragrafos(docx))
    titulo = next((p["texto"] for p in pars if re.fullmatch(r"(?:[A-ZÇÃÕÉÊÁÍÓÚ] ){3,}[A-ZÇÃÕÉÊÁÍÓÚ]", p["texto"])), "")
    ato = "sentença" if "S E N T" in titulo else "decisão" if "D E C I S" in titulo else "despacho"
    processo = next((comum.numero_cnj(p["texto"]) for p in pars if comum.numero_cnj(p["texto"])), None)
    out = [f"// modelo importado de: {arq.name}", f"@ato {ato}"] + ([f"@processo {processo}"] if processo else [])
    comecou = terminou = corpo_iniciado = False
    for p in pars:
        t = p["texto"]
        if not comecou:
            out_cab = f"// cabeçalho: {t}"
            if t == titulo and titulo:  # o corpo começa logo depois do título (S E N T E N Ç A, D E S P A C H O…)
                comecou = True
                out.append(out_cab)
                continue
            if re.match(r"^(\d+\.\s*)?Trata-se\b", t) or re.match(r"^(Vistos|Cuida-se|Tratam os autos)", t):
                comecou = True
            else:
                out.append(out_cab)
                continue
        if not corpo_iniciado and re.match(r"^[A-ZÇÃÕÉÊÁÍÓÚÂÔ /]{3,}:\s", t):
            out.append(f"// cabeçalho: {t}")  # "AUTOR: …", "RÉU: …" abaixo do título continuam cabeçalho
            continue
        if not terminou and re.search(r"datado eletronicamente|^JUIZA? DE DIREITO$", t):
            terminou = True  # local, data e assinatura vêm do modelo do SAJ
        if terminou:
            out.append(f"// rodapé: {t}")
            continue
        visiveis = [r for r in p["runs"] if r["t"].strip()]
        courier = bool(visiveis) and sum(r["courier"] for r in visiveis) > len(visiveis) / 2
        enumerador = re.match(r"^(?:\d{1,3}\.\s*)?(?:[ivxl]+|[a-z])\)", t)
        item = not courier and p["recuo"] >= 1500 and bool(enumerador)  # enumeração recuada em Times
        cit = courier or (p["recuo"] >= 1500 and not item)  # transcrição recuada, ainda que em Times
        todo_b = bool(visiveis) and all(r["b"] for r in visiveis)
        todo_u = bool(visiveis) and all(r["u"] for r in visiveis)
        if cit:
            out.append("> " + _inline(p["runs"]))
        elif item:
            out.append(("++ " if p["recuo"] >= 2400 else "+ ") + _inline(p["runs"], tirar=("u",) if todo_u else ()))
        elif re.match(r"^(Diante do exposto|Do exposto|Ante o exposto|Pelo exposto)", t):
            out.append(_inline(p["runs"], tirar=("b", "u")))
        elif re.fullmatch(r"É o [Rr]elatório\.", t):
            out.append(t)
        elif todo_b and todo_u:
            out.append("!! " + _inline(p["runs"], tirar=("b", "u")))
        elif todo_u:
            out.append("__ " + _inline(p["runs"], tirar=("u",)))
        else:
            out.append(_inline(p["runs"]))
        if not cit:  # numeração digitada à mão no modelo ("5.", "**6.**", "__9.__") não entra na marcação
            def _sem_numero(m):
                abre, fecha = m.group(2), m.group(3)
                return m.group(1) + ("" if fecha else abre)  # "**7. Não havendo**" → "**Não havendo**"
            out[-1] = re.sub(r"^((?:!! |__ |\+\+ |\+ )?)((?:\*\*|__)*)\d{1,3}\.((?:\*\*|__)*)\s+", _sem_numero, out[-1])
        corpo_iniciado = True
        if re.fullmatch(r"P\. ?R\. ?I\.|Cumpra-se(,? observada a sequência acima)?\.", t):
            terminou = True
    return "\n".join(out) + "\n"


def _pastas_modelos():
    pastas = [RAIZ / "modelos"]
    for x in comum.config()["pastas"].get("modelos_usuario") or []:
        if Path(x).expanduser().is_dir():
            pastas.append(Path(x).expanduser())
    return pastas


def buscar(argv):
    maximo = int(comum.arg(argv, "--max", 8))
    termos = [comum.sem_acento(t.lower()) for t in re.findall(r"[\wÀ-ÿ]{3,}", " ".join(argv))]
    resultado = []
    for pasta in _pastas_modelos():
        for arq in pasta.rglob("*"):
            if arq.suffix.lower() not in (".txt", ".docx", ".rtf", ".odt", ".doc") or arq.name.startswith("~$"):
                continue
            nome = comum.sem_acento(arq.stem.lower().replace("_", " "))
            amostra = ""
            if arq.suffix.lower() == ".txt":
                amostra = comum.sem_acento(arq.read_text(encoding="utf-8", errors="replace")[:6000].lower())
            pontos = sum(3 for t in termos if t in nome) + sum(1 for t in termos if t in amostra)
            if pontos:
                resultado.append((pontos, str(arq)))
    resultado.sort(key=lambda x: (-x[0], x[1]))
    print(json.dumps([{"pontos": p, "arquivo": a} for p, a in resultado[:maximo]], ensure_ascii=False, indent=1))
    return 0


def main(argv):
    comum.utf8_console()
    if not argv:
        print(__doc__)
        return 2
    if argv[0] == "buscar":
        return buscar(argv[1:])
    arq = Path(argv.pop(0)).resolve()
    saida = comum.arg(argv, "--saida")
    texto = importar(arq)
    if saida:
        Path(saida).write_text(texto, encoding="utf-8")
        print(saida)
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
