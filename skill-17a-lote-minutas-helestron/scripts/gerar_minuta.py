#!/usr/bin/env python3
"""Gera a minuta em Word (.docx) a partir da marcação (referencias/formato_minuta.md).

Uso:
  python -I gerar_minuta.py <minuta.txt> --saida <pasta> [--nome Minuta_<n>_<ato>] [--rascunho]

Saídas (na pasta indicada):
  <nome>_anotada.docx  com os apontamentos em vermelho, as notas e a ressalva de apoio (para revisão)
  <nome>.docx          versão limpa, pronta para copiar no editor do SAJ (sem vermelho, salvo o
                       parêntese Sisbajud/Renajud marcado com {{! }})

Formatação (config/vara.json > formatacao, medida nos modelos da vara): A4; Times New Roman 12;
recuo de 2,5 cm na primeira linha; entrelinhas 1,5; justificado; transcrições em Courier New 10,
recuo esquerdo de 4 cm, espaçamento simples. **Sem numeração de parágrafos** — o usuário a aplica
no SAJ. Antes de gerar, roda o portão (verificar_minuta.py); com pendência bloqueante, não gera
nada (com --rascunho, gera só a anotada, com as pendências no topo). Depois de gerar, confere o XML
das duas versões e imprime o resultado em JSON.
Só biblioteca padrão (zipfile + XML).
"""
import json
import re
import sys
sys.dont_write_bytecode = True
import zipfile
from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402
import marcacao  # noqa: E402
import verificar_minuta  # noqa: E402

RAIZ = Path(__file__).resolve().parent
TW = 567  # twips por centímetro


def _termos_italico():
    arq = RAIZ / "termos_italico.txt"
    termos = [t.strip() for t in arq.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]
    termos.sort(key=len, reverse=True)
    return re.compile(r"(?<![\wÀ-ÿ])(" + "|".join(re.escape(t) for t in termos) + r")(?![\wÀ-ÿ])", re.I)


ITALICO_RE = _termos_italico()


def _italicizar(trechos):
    """Aplica itálico automático aos termos estrangeiros dos trechos ainda sem itálico."""
    out = []
    for r in trechos:
        if r["i"] or r["red"]:
            out.append(r)
            continue
        pos = 0
        for m in ITALICO_RE.finditer(r["t"]):
            if m.start() > pos:
                out.append({**r, "t": r["t"][pos:m.start()]})
            out.append({**r, "t": m.group(0), "i": True})
            pos = m.end()
        if pos < len(r["t"]):
            out.append({**r, "t": r["t"][pos:]})
    return out


def _fmt():
    f = comum.config()["formatacao"]
    return {
        "fonte": f["fonte"], "sz": int(f["corpo_pt"] * 2),
        "recuo": int(f["recuo_primeira_linha_cm"] * TW), "linha": int(240 * f["entrelinhas"]),
        "antes": int(f["espaco_antes_pt"] * 20), "depois": int(f["espaco_depois_pt"] * 20),
        "cfonte": f["citacao_fonte"], "csz": int(f["citacao_pt"] * 2),
        "crecuo": int(f["citacao_recuo_esquerdo_cm"] * TW), "clinha": int(240 * f["citacao_entrelinhas"]),
        "cesp": int(f["citacao_espaco_pt"] * 20),
        "margens": [int(f[k] * TW) for k in ("margem_superior_cm", "margem_direita_cm", "margem_inferior_cm",
                                            "margem_esquerda_cm")],
    }


def _ppr(k, F):
    if k == "cit":
        return (f'<w:pPr><w:spacing w:before="{F["cesp"]}" w:after="{F["cesp"]}" w:line="{F["clinha"]}" '
                f'w:lineRule="auto"/><w:ind w:left="{F["crecuo"]}"/><w:jc w:val="both"/></w:pPr>')
    if k in ("nota", "cabecalho"):
        return '<w:pPr><w:spacing w:before="60" w:after="60"/><w:jc w:val="both"/></w:pPr>'
    return (f'<w:pPr><w:spacing w:before="{F["antes"]}" w:after="{F["depois"]}" w:line="{F["linha"]}" '
            f'w:lineRule="auto"/><w:ind w:firstLine="{F["recuo"]}"/><w:jc w:val="both"/></w:pPr>')


def _rpr(fonte, sz, b=False, i=False, u=False, red=False):
    x = f'<w:rFonts w:ascii="{fonte}" w:hAnsi="{fonte}" w:cs="{fonte}" w:eastAsia="{fonte}"/>'
    if b:
        x += "<w:b/><w:bCs/>"
    if i:
        x += "<w:i/><w:iCs/>"
    if u:
        x += '<w:u w:val="single"/>'
    if red:
        x += '<w:color w:val="FF0000"/>'
    return f"<w:rPr>{x}<w:sz w:val=\"{sz}\"/><w:szCs w:val=\"{sz}\"/><w:lang w:val=\"pt-BR\"/></w:rPr>"


def _paragrafo(p, anotada, F):
    k = p["k"]
    if k == "nota" and not anotada:
        return ""
    trechos = _italicizar(marcacao.runs(p["txt"]))
    if not anotada:
        trechos = [r for r in trechos if not r["red"] or r["fica"]]
    fonte, sz = (F["cfonte"], F["csz"]) if k == "cit" else (F["fonte"], F["sz"])
    todo_b = k in ("decisorio", "dispositivo", "relatorio")
    todo_u = k in ("decisorio", "dispositivo", "sublinhado", "comando")
    todo_red = k in ("nota", "cabecalho")
    corpo = []
    for r in trechos:
        texto = r["t"]
        if r["red"] and not r["fica"]:
            texto = " " + texto.strip() + " "
        if not texto:
            continue
        red = todo_red or r["red"]
        b = (todo_b or r["b"] or (r["red"] and not r["fica"]) or todo_red) and not (k == "comando" and not r["b"])
        u = (todo_u or r["u"]) and not r["red"]
        corpo.append(f'<w:r>{_rpr(fonte, sz, b, r["i"], u, red)}<w:t xml:space="preserve">{escape(texto)}</w:t></w:r>')
    if not corpo:
        return ""
    return f"<w:p>{_ppr(k, F)}{''.join(corpo)}</w:p>"


def _documento(pars, anotada, F, cabecalho):
    corpo = []
    if anotada:
        for linha in cabecalho:
            corpo.append(_paragrafo({"k": "cabecalho", "txt": linha}, True, F))
    for p in pars:
        corpo.append(_paragrafo(p, anotada, F))
    if anotada:
        notas = (RAIZ / "notas_anotada.txt").read_text(encoding="utf-8").splitlines()
        for n in notas:
            if n.strip():
                corpo.append(_paragrafo({"k": "nota", "txt": n.strip()}, True, F))
    m = F["margens"]
    sect = (f'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="{m[0]}" w:right="{m[1]}" '
            f'w:bottom="{m[2]}" w:left="{m[3]}" w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:body>{"".join(c for c in corpo if c)}{sect}</w:body></w:document>')


def _estilos(F):
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            f'<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="{F["fonte"]}" w:hAnsi="{F["fonte"]}" '
            f'w:cs="{F["fonte"]}" w:eastAsia="{F["fonte"]}"/><w:sz w:val="{F["sz"]}"/><w:szCs w:val="{F["sz"]}"/>'
            '<w:lang w:val="pt-BR" w:eastAsia="pt-BR" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr></w:pPrDefault>'
            '</w:docDefaults><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/>'
            '<w:qFormat/></w:style></w:styles>')


def _gravar_docx(destino: Path, documento: str, estilos: str, titulo: str):
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
          '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
          '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
          '</Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '</Relationships>')
    drels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
             '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
             '</Relationships>')
    agora = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    core = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            f'<dc:title>{escape(titulo)}</dc:title><dc:creator>17ª Vara Cível da Capital — minuta de apoio</dc:creator>'
            f'<dc:language>pt-BR</dc:language><dcterms:created xsi:type="dcterms:W3CDTF">{agora}</dcterms:created>'
            '</cp:coreProperties>')
    destino.parent.mkdir(parents=True, exist_ok=True)
    tmp = destino.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", drels)
        z.writestr("word/document.xml", documento)
        z.writestr("word/styles.xml", estilos)
        z.writestr("docProps/core.xml", core)
    tmp.replace(destino)


def conferir_xml(limpa: Path, anotada: Path, pars) -> list:
    """Conferência do XML gerado: nada de vermelho de apontamento, nota ou marca na limpa;
    dispositivo em negrito e sublinhado; transcrições em Courier New com recuo."""
    erros = []
    with zipfile.ZipFile(limpa) as z:
        x = z.read("word/document.xml").decode("utf-8")
    fica = sum(1 for p in pars for r in marcacao.runs(p["txt"]) if r["fica"])
    vermelhos = x.count('w:color w:val="FF0000"')
    if vermelhos and not fica:
        erros.append("vermelho na versão limpa")
    for marca in ("{{", "}}", "**", "%%", "Conferir:"):
        if marca in x:
            erros.append(f"marca '{marca}' na versão limpa")
    if re.search(r"<w:numPr>", x):
        erros.append("numeração automática na versão limpa")
    if any(p["k"] == "cit" for p in pars) and "Courier New" not in x:
        erros.append("transcrição sem Courier New")
    disp = next((p for p in pars if p["k"] == "dispositivo"), None)
    if disp:
        inicio = marcacao.sem_marcas(disp["txt"])[:30]
        for par in re.findall(r"<w:p>.*?</w:p>", x, re.S):
            texto = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", par))
            if texto.startswith(escape(inicio)):
                corridas = re.findall(r"<w:r>.*?</w:r>", par, re.S)
                if not all("<w:b/>" in c and "<w:u " in c for c in corridas):
                    erros.append("dispositivo sem negrito e sublinhado")
                break
        else:
            erros.append("dispositivo não encontrado na versão limpa")
    with zipfile.ZipFile(anotada) as z:
        xa = z.read("word/document.xml").decode("utf-8")
    if any("{{" in p["txt"] for p in pars) and 'w:color w:val="FF0000"' not in xa:
        erros.append("apontamentos sem vermelho na anotada")
    return erros


def main(argv):
    comum.utf8_console()
    if not argv or argv[0].startswith("-"):
        print(__doc__)
        return 2
    entrada = Path(argv.pop(0)).resolve()
    saida = Path(comum.arg(argv, "--saida") or entrada.parent).resolve()
    nome = comum.arg(argv, "--nome")
    rascunho = comum.flag(argv, "--rascunho")
    m = marcacao.ler(entrada)
    if not nome:
        ato = comum.sem_acento(m["ato"] or "minuta").replace(" ", "_")
        nome = f"Minuta_{m['processo']}_{ato}" if m["processo"] else entrada.stem
    veredito = verificar_minuta.verificar(entrada)
    F = _fmt()
    cab = [f"Minuta de {m['ato'] or 'ato'} — processo {m['processo'] or '[número]'} — versão anotada para revisão"]
    if veredito["resultado"] != "OK":
        if not rascunho:
            print(json.dumps({"resultado": "BLOQUEADO", "motivo": "pendências do portão; corrija o .txt e gere de novo",
                              "pendencias_bloqueantes": veredito["pendencias_bloqueantes"]}, ensure_ascii=False, indent=1))
            return 1
        cab += [f"PENDÊNCIA: {x}" for x in veredito["pendencias_bloqueantes"]]
    anotada = saida / f"{nome}_anotada.docx"
    _gravar_docx(anotada, _documento(m["pars"], True, F, cab), _estilos(F), nome)
    if rascunho and veredito["resultado"] != "OK":
        print(json.dumps({"resultado": "RASCUNHO", "anotada": str(anotada)}, ensure_ascii=False, indent=1))
        return 1
    limpa = saida / f"{nome}.docx"
    _gravar_docx(limpa, _documento(m["pars"], False, F, []), _estilos(F), nome)
    erros = conferir_xml(limpa, anotada, m["pars"])
    if erros:
        limpa.unlink()
    print(json.dumps({"resultado": "OK" if not erros else "FALHA_XML", "erros_xml": erros,
                      "anotada": str(anotada), "limpa": None if erros else str(limpa),
                      "apontamentos": veredito["apontamentos"]}, ensure_ascii=False, indent=1))
    return 0 if not erros else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
