#!/usr/bin/env python3
"""Autos em PDF já baixados pelo Helestron: inventário, lote de 10, texto, mapa, leitura dirigida e
transcrições de audiências.

Fase 1 do SKILL.md. Nada se baixa e nada se acessa no e-SAJ: lê-se a pasta de downloads do
Helestron (o acervo ou a pasta de um lote), compartilhada com a sessão. PDFs, `_texto`, capas e
`_controle/` do Helestron são SOMENTE LEITURA — o script grava só na pasta de trabalho
(`<downloads>/_Vara17/trabalho`, salvo `--trabalho`).

Subcomandos (todos aceitam --trabalho <dir>; o inventário cria e imprime a pasta):
  inventario [<pasta>] [--lista N1 N2 …] [--lista-arquivo f] [--lote 10] [--novo-lote] [--transcricoes <pasta>]
        Sem <pasta>, usa a do Helestron (config ou `caminhos --json`). Localiza os PDFs (nome = número
        CNJ; incidente com sufixo -NN), associa texto, capa e registro do Helestron e as transcrições
        de audiência, isola os sigilosos e forma o lote (até 10): a lista do usuário, na ordem dada;
        sem lista, os pendentes por prioridade legal, conclusão mais antiga e data do download.
  preparar [N …]          texto com marcas de folha (o do Helestron; senão, `helestron preparar`;
                          senão, extração própria) e mapa de cada processo do lote
  mapa N | capa N | caminhos N
  ler N --fls A-B | --peca REGEX [--max 40000]
  buscar N REGEX [--contexto 250] [--max 30]
  transcricoes N [--ler [i]] [--max 60000]   lista as transcrições do processo; --ler mostra a i-ésima
  requisitos N            cumprimento de sentença: pistas, com as fls., de cada requisito do requerimento
                          (art. 534 do CPC e Resolução TJAL n.º 21/2023), da habilitação de sucessores e
                          da fase (impugnação, requisitório, cessão), no processo e nos autos relacionados
  relacionados N          autos de origem e demais sequenciais do mesmo número (título, fases anteriores)
  autorizar N --ordem "texto literal da autorização do magistrado"   (sigiloso; vale no dia)
  marcar N ETAPA [--ato X] [--resultado TXT] [--alerta TXT] [--minuta PATH] [--justificativa TXT]
  status | relatorio
  validar N1 N2 …         confere formato, dígito verificador e foro dos números

`N` aceita o número CNJ (completo ou NNNNNNN-DD.AAAA) ou a posição no lote. Etapas: pendente →
preparado → analisado → pesquisado → minutado → revisado → entregue (ou falhou). A retomada é
idempotente: nada que já esteja concluído se refaz.
"""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
sys.dont_write_bytecode = True
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402
import ponte_helestron as ph  # noqa: E402

ETAPAS = ["pendente", "preparado", "analisado", "pesquisado", "minutado", "revisado", "entregue", "falhou"]
MARCA = re.compile(r"^=== \[(.+?)\](?: \(pág\. (\d+) do PDF\))? ===\s*$")
DOC = re.compile(r"^\[documento:\s*(.+?)\]\s*$")
SEM_TEXTO = re.compile(r"^\[página sem texto extraível")
AUSENTE = re.compile(r"^\[folha não disponível no e-SAJ:\s*(.+?)\]")
CLASSES = [
    ("Mandado de Segurança", r"mandado\s+de\s+seguran[çc]a"),
    ("Execução Fiscal", r"execu[çc][ãa]o\s+fiscal"),
    ("Embargos à Execução Fiscal", r"embargos\s+[àa]\s+execu[çc][ãa]o\s+fiscal"),
    ("Embargos à Execução", r"embargos\s+[àa]\s+execu[çc][ãa]o"),
    ("Cumprimento de Sentença contra a Fazenda Pública", r"cumprimento\s+de\s+senten[çc]a\s+contra\s+a\s+fazenda"),
    ("Cumprimento de Sentença", r"cumprimento\s+(?:provis[óo]rio\s+)?de\s+senten[çc]a"),
    ("Liquidação de Sentença", r"liquida[çc][ãa]o\s+(?:de|por)\s+"),
    ("Ação Civil Pública", r"a[çc][ãa]o\s+civil\s+p[úu]blica"),
    ("Ação Popular", r"a[çc][ãa]o\s+popular"),
    ("Desapropriação", r"desapropria[çc][ãa]o"),
    ("Improbidade Administrativa", r"improbidade"),
    ("Tutela Cautelar Antecedente", r"tutela\s+cautelar\s+antecedente"),
    ("Embargos de Terceiro", r"embargos\s+de\s+terceiro"),
    ("Procedimento Comum Cível", r"procedimento\s+comum"),
]
PISTAS = {
    "tutela de urgência / liminar": r"tutela de urg[êe]ncia|tutela provis[óo]ria|\bliminar",
    "contestação": r"\bcontesta[çc][ãa]o\b",
    "réplica": r"\br[ée]plica\b|impugna[çc][ãa]o [àa] contesta",
    "audiência": r"\baudi[êe]ncia\b|termo de audi",
    "perícia / laudo": r"\blaudo\b|per[íi]cia|perito",
    "sentença / decisão": r"\bsenten[çc]a\b|julgo (?:im)?procedente|\bdecis[ãa]o\b",
    "embargos de declaração": r"embargos de declara[çc][ãa]o",
    "cálculos / RPV / precatório": r"c[áa]lculo|planilha|\bRPV\b|precat[óo]rio|requisi[çc][ãa]o de pequeno",
    "prescrição / decadência": r"prescri[çc]|decad[êe]ncia",
    "gratuidade": r"gratuidade|justi[çc]a gratuita|assist[êe]ncia judici[áa]ria",
    "Ministério Público": r"minist[ée]rio p[úu]blico|promotor|parecer ministerial",
    "acordo / transação": r"\bacordo\b|transa[çc][ãa]o|concilia[çc][ãa]o",
    "suspensão / IRDR / tema": r"sobrest|suspens[ãa]o do (?:feito|processo)|\bIRDR\b|\btema\s+\d",
    "trânsito em julgado": r"tr[âa]nsito em julgado|transitou",
    "recurso": r"\bapela[çc][ãa]o\b|agravo de instrumento|recurso especial|recurso extraordin",
    "óbito / habilitação": r"[óo]bito|falecimento|habilita[çc][ãa]o de herdeiros",
}


# ---------------------------------------------------------------- estado

def caminho_estado(trab: Path) -> Path:
    return trab / "estado.json"


def carregar_estado(trab: Path) -> dict:
    est = comum.ler_json(caminho_estado(trab))
    if not est:
        sys.exit(f"Sem estado em {trab}: rode antes `autos.py inventario`.")
    return est


def salvar_estado(trab: Path, est: dict):
    est["atualizado"] = datetime.now().isoformat(timespec="seconds")
    comum.gravar_json(caminho_estado(trab), est)


def lote_corrente(est: dict):
    return est["lotes"][-1] if est.get("lotes") else None


def autorizado(est: dict, n: str) -> bool:
    a = est.get("autorizados", {}).get(n)
    return bool(a) and a.get("data") == comum.hoje()


def alias_sigiloso(n: str) -> str:
    """Identificador do sigiloso fora da pasta dele (o número real fica só lá)."""
    return "SIG-" + hashlib.sha1(n.encode()).hexdigest()[:6]


def proc(est: dict, n: str) -> dict:
    alvo = comum.completar_cnj(n) or n
    for chave in (alvo, alias_sigiloso(alvo), n):
        if chave in est["processos"]:
            return est["processos"][chave]
    lote = lote_corrente(est)
    if lote and n.isdigit() and 1 <= int(n) <= len(lote["numeros"]):
        return est["processos"][lote["numeros"][int(n) - 1]]
    sys.exit(f"Processo {n} não está no inventário.")


def guarda_sigilo(est: dict, p: dict):
    if p.get("sigiloso") and not autorizado(est, p["numero"]):
        sys.exit(f"Posição {p.get('posicao', '?')}: processo em segredo de justiça — aguardando autorização "
                 "expressa do magistrado (autos.py autorizar). Nada foi lido.")


def dados(est: dict, p: dict) -> dict:
    """Dados de leitura do processo; do sigiloso, só com autorização, lidos na pasta dele."""
    guarda_sigilo(est, p)
    if not p.get("ref"):
        return p
    reais = comum.ler_json(p["ref"], {}).get(p["numero"], {})
    return {**p, **reais, "numero": reais.get("numero_real", p["numero"])}


def pasta_proc(trab: Path, p: dict) -> Path:
    if p.get("ref"):
        return Path(p["ref"]).parent / "autos" / p["numero"]
    return trab / "autos" / p["numero"]


def pasta_minutas(est: dict, p: dict) -> Path:
    lote = p.get("lote") or lote_corrente(est)["id"]
    if p.get("ref"):
        return Path(p["ref"]).parent / "minutas" / lote
    return Path(est["minutas"]) / lote


# ---------------------------------------------------------------- autos relacionados (cumprimento de sentença)

def base_cnj(n: str) -> str:
    """Número sem o sufixo do incidente: 0724179-30.2017.8.02.0001-01 → 0724179-30.2017.8.02.0001."""
    return n[:25]


def relacionados(est: dict, n: str) -> list:
    """Processo de conhecimento e demais sequenciais do mesmo número presentes na pasta."""
    return sorted(k for k in est["processos"] if k != n and not k.startswith("SIG-") and base_cnj(k) == base_cnj(n))


def com_apoio(est: dict, numeros: list) -> list:
    """Números do lote seguidos dos autos relacionados (apoio: não contam no lote nem geram minuta)."""
    out = []
    for n in numeros:
        for x in [n] + (relacionados(est, n) if not n.startswith("SIG-") else []):
            if x not in out:
                out.append(x)
    return out


# ---------------------------------------------------------------- inventário

def _achar(diretorio: Path, stem: str, seq: str, sufixo: str, palavra: str = ""):
    """Arquivo associado ao PDF em _texto/, _controle/ ou no próprio diretório (nome exato; depois,
    o que traga o número e a palavra). Para o texto, descarta capa, meta e relatório."""
    bases = [b for b in (diretorio / "_texto", diretorio / "_controle", diretorio) if b.is_dir()]
    nome_exato = f"{stem}_{palavra}{sufixo}" if palavra else f"{stem}{sufixo}"
    for base in bases:
        if (base / nome_exato).exists() and (palavra or base.name == "_texto" or base == diretorio):
            return base / nome_exato
    alvo = comum.numero_cnj(stem)
    for base in bases:
        for f in sorted(base.glob(f"*{seq}*{sufixo}")):
            if alvo and comum.numero_cnj(f.name) != alvo:
                continue  # o incidente (-01) não herda a capa nem o texto do principal, e vice-versa
            nome = f.name.lower()
            if palavra and palavra in nome:
                return f
            if not palavra and not any(x in nome for x in ("capa", "meta", "relatorio", "saida")):
                return f
    return None


def _capa_info(caminho):
    info = {"classe": None, "assunto": None, "sigiloso": False, "prioridade": False, "conclusao": None,
            "audiencias": 0}
    if not caminho:
        return info
    try:
        d = json.loads(Path(caminho).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        info["sigiloso"] = True  # capa ilegível: trata-se como sigilosa até conferência
        return info
    info["sigiloso"] = bool(d.get("sigiloso") or d.get("segredo"))
    if info["sigiloso"]:
        return info  # nada mais se lê do sigiloso
    capa = d.get("capa") or {}
    info["classe"] = capa.get("classe")
    info["assunto"] = capa.get("assunto")
    info["prioridade"] = bool(d.get("prioridade") or d.get("idoso"))
    info["audiencias"] = len(d.get("audiencias") or [])
    for mov in d.get("movimentacoes") or []:
        s = json.dumps(mov, ensure_ascii=False)
        if re.search(r"conclus", s, re.I):
            m = re.search(r"(\d{2})/(\d{2})/(\d{4})", s)
            if m:
                data = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
                info["conclusao"] = max(info["conclusao"] or data, data)
    return info


def _classe_do_texto(amostra: str):
    for nome, rx in CLASSES:
        if re.search(rx, amostra or "", re.I):
            return nome
    return None


def _sigilosos_csv(pasta: Path) -> int:
    total = 0
    for f in list(pasta.rglob("relatorio*.csv"))[:50]:
        try:
            with open(f, encoding="utf-8-sig", newline="") as fh:
                total += sum(1 for r in csv.DictReader(fh, delimiter=";")
                             if (r.get("sigiloso") or "").lower() == "sim" or "processo sigiloso" in (r.get("processo") or ""))
        except (OSError, csv.Error):
            pass
    return total


def _pasta_saida(pasta: Path, argv) -> Path:
    explicito = "--trabalho" in argv or "-t" in argv or os.environ.get("VARA17_TRABALHO")
    if explicito:
        return comum.pasta_trabalho(argv, criar=True)
    cfg = comum.config()["pastas"].get("saida")
    base = Path(cfg).expanduser() if cfg else pasta / "_Vara17"
    trab = base / "trabalho"
    try:
        trab.mkdir(parents=True, exist_ok=True)
        teste = trab / ".escrita"
        teste.write_text("ok", encoding="utf-8")
        teste.unlink()
    except OSError:
        trab = Path.cwd() / "_Vara17" / "trabalho"
        trab.mkdir(parents=True, exist_ok=True)
    return trab


def inventario(argv):
    pasta_arg = argv.pop(0) if argv and not argv[0].startswith("-") else None
    tam = int(comum.arg(argv, "--lote", comum.config()["lote"]["tamanho"]))
    lista_arq = comum.arg(argv, "--lista-arquivo")
    transc_arg = comum.arg(argv, "--transcricoes")
    novo = comum.flag(argv, "--novo-lote")
    lista = []
    if "--lista" in argv:
        i = argv.index("--lista")
        j = i + 1
        while j < len(argv) and not argv[j].startswith("-"):
            j += 1
        lista = argv[i + 1:j]
        del argv[i:j]
    if lista_arq:
        lista += comum.extrair_numeros(Path(lista_arq).read_text(encoding="utf-8", errors="replace"))
    lista = [comum.completar_cnj(x) or x for x in lista]

    pasta = ph.pasta_downloads(pasta_arg)
    if not pasta:
        sys.exit("Pasta de downloads do Helestron não localizada: informe-a (autos.py inventario \"<pasta>\") "
                 "ou, no Cowork, conecte-a à sessão.")
    trab = _pasta_saida(pasta, argv)
    est = comum.ler_json(caminho_estado(trab)) or {"processos": {}, "lotes": [], "autorizados": {}}
    est.update({"pasta_helestron": str(pasta), "trabalho": str(trab), "minutas": str(trab.parent / "minutas")})

    transc = ph.pasta_transcricoes(transc_arg, pasta)
    idx_transc = ph.indexar_transcricoes(transc) if transc else {}
    est["pasta_transcricoes"] = str(transc) if transc else None

    achados, sem_numero = {}, 0
    ignorar = {"_Vara17", "_texto", "_controle", "_capa", "_minutas"}
    raizes = [(pasta, False)]
    sig = ph.pasta_sigilosos()  # o Helestron guarda os sigilosos fora do acervo
    if sig and pasta not in sig.parents and sig != pasta and sig not in pasta.parents:
        raizes.append((sig, True))
    for base, toda_sigilosa in raizes:
        for raiz, dirs, arqs in os.walk(base):
            r = Path(raiz)
            sigilo_dir = toda_sigilosa or any("sigilos" in parte.lower() for parte in r.relative_to(base).parts)
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ignorar]
            for a in arqs:
                if not a.lower().endswith(".pdf"):
                    continue
                n = comum.numero_cnj(Path(a).stem) or comum.numero_cnj(r.name)
                if not n:
                    sem_numero += 1
                    continue
                achados.setdefault(n, {"pdfs": [], "sigilo_dir": False})
                achados[n]["pdfs"].append(str(r / a))
                achados[n]["sigilo_dir"] |= sigilo_dir

    for n, a in achados.items():
        a["pdfs"].sort()
        pdf0 = Path(a["pdfs"][0])
        seq = n.split("-")[0]
        texto = _achar(pdf0.parent, pdf0.stem, seq, ".txt")
        capa = _achar(pdf0.parent, pdf0.stem, seq, ".json", "capa")
        meta = _achar(pdf0.parent, pdf0.stem, seq, ".json", "meta")
        info = _capa_info(capa)
        transcricoes = idx_transc.get(n, [])
        sigiloso = info["sigiloso"] or a["sigilo_dir"] or any(t["sigilosa"] for t in transcricoes)
        if sigiloso:  # número e caminhos só na pasta do próprio sigiloso
            alias = alias_sigiloso(n)
            ref = pdf0.parent / "_Vara17" / "estado_sigilosos.json"
            try:
                reais = comum.ler_json(ref, {})
                reais[alias] = {"numero_real": n, "pdfs": a["pdfs"], "texto_helestron": str(texto) if texto else None,
                                "capa": str(capa) if capa else None, "meta": str(meta) if meta else None,
                                "transcricoes": transcricoes}
                comum.gravar_json(ref, reais)
            except OSError:
                ref = None
            p = est["processos"].get(alias, {"numero": alias, "etapa": "pendente"})
            p.update({"sigiloso": True, "ref": str(ref) if ref else None, "mtime": os.path.getmtime(pdf0)})
            est["processos"][alias] = p
            continue
        p = est["processos"].get(n, {"numero": n, "etapa": "pendente"})
        p.update({"pdfs": a["pdfs"], "texto_helestron": str(texto) if texto else None,
                  "capa": str(capa) if capa else None, "meta": str(meta) if meta else None,
                  "sigiloso": False, "prioridade": info["prioridade"], "conclusao": info["conclusao"],
                  "audiencias_capa": info["audiencias"], "transcricoes": transcricoes,
                  "mtime": os.path.getmtime(pdf0)})
        p["classe"] = info["classe"] or p.get("classe")
        p["assunto"] = info["assunto"] or p.get("assunto")
        est["processos"][n] = p

    def chave(p):
        return (0 if p.get("prioridade") else 1, p.get("conclusao") or "9999", p.get("mtime") or 0)

    invalidos = [f"{x} ({comum.validar_cnj(x).get('motivo', 'inválido')})" for x in lista
                 if not comum.validar_cnj(x)["valido"]]
    lista = [x for x in lista if comum.validar_cnj(x)["valido"]]
    normal = [alias_sigiloso(x) if alias_sigiloso(x) in est["processos"] else x for x in lista]
    nao_achados = [x for x in normal if x not in est["processos"]]
    candidatos = [n for n in normal if n in est["processos"]] if normal else \
        sorted(est["processos"], key=lambda k: chave(est["processos"][k]))

    lote = lote_corrente(est)
    aberto = lote and any(est["processos"].get(n, {}).get("etapa") not in ("entregue", "falhou", None)
                          for n in lote["numeros"])
    mesma_lista = bool(normal) and lote and lote["numeros"] == candidatos[:tam]
    if novo or not aberto or (normal and not mesma_lista):  # a mesma lista retoma o lote aberto
        numeros = (candidatos if normal else
                   [n for n in candidatos if est["processos"][n]["etapa"] not in ("entregue", "falhou")])[:tam]
        seq_lote = sum(1 for lt in est["lotes"] if lt["id"].startswith(comum.hoje())) + 1
        lote = {"id": f"{comum.hoje()}_lote{seq_lote:02d}", "criado": datetime.now().isoformat(timespec="seconds"),
                "numeros": numeros, "nao_encontrados": nao_achados, "excedentes": candidatos[tam:] if normal else []}
        est["lotes"].append(lote)
    for i, n in enumerate(lote["numeros"], 1):
        est["processos"][n]["posicao"] = i
        est["processos"][n]["lote"] = lote["id"]
    salvar_estado(trab, est)

    print(f"TRABALHO={trab.as_posix()}")
    print(f"MINUTAS={(Path(est['minutas']) / lote['id']).as_posix()}  (sigiloso: a saída de `autos.py caminhos N`)")
    print(f"TRANSCRICOES={transc.as_posix() if transc else '(não localizada)'}")
    pend = sum(1 for p in est["processos"].values() if p["etapa"] not in ("entregue", "falhou"))
    print(f"processos na pasta: {len(est['processos'])} (pendentes: {pend}); PDFs sem número CNJ no nome: "
          f"{sem_numero}; sigilosos no relatório do Helestron: {_sigilosos_csv(pasta)}")
    if invalidos:
        print("da lista, números inválidos (não trabalhados): " + "; ".join(invalidos))
    if nao_achados:
        print("da lista, não encontrados na pasta (baixe-os pelo Helestron): " + ", ".join(nao_achados))
    if lote.get("excedentes"):
        print("excedentes (próximo lote): " + ", ".join(lote["excedentes"]))
    print(f"LOTE {lote['id']} ({len(lote['numeros'])}):")
    for i, n in enumerate(lote["numeros"], 1):
        p = est["processos"][n]
        if p.get("sigiloso") and not autorizado(est, n):
            print(f"{i:2d}. (processo sigiloso) — aguardando autorização")
            continue
        val = comum.validar_cnj(n)
        rel = relacionados(est, n)
        p["relacionados"] = rel
        cs = len(n) > 25 or re.search(r"(?i)cumprimento", p.get("classe") or "")
        p["cumprimento"] = bool(cs)
        sem_origem = len(n) > 25 and base_cnj(n) not in est["processos"]
        flags = [f for f, v in (("prioridade", p.get("prioridade")),
                                ("cumprimento de sentença", cs),
                                (f"apoio: {', '.join(rel)}", rel),
                                (f"AUTOS DE ORIGEM AUSENTES ({base_cnj(n)}): baixe-os pelo Helestron", sem_origem),
                                ("sem texto do Helestron", not p.get("texto_helestron")),
                                (f"{len(p.get('transcricoes') or [])} transcrição(ões)", p.get("transcricoes")),
                                (val.get("aviso") or val.get("motivo"), val.get("aviso") or not val["valido"])) if v]
        print(f"{i:2d}. {n} | {p.get('classe') or 'classe ?'} | {p['etapa']}" + (f" | {'; '.join(flags)}" if flags else ""))
    salvar_estado(trab, est)
    return 0


# ---------------------------------------------------------------- texto e mapa

def arquivo_texto(trab: Path, p: dict, d: dict) -> Path:
    h = d.get("texto_helestron")
    if h and Path(h).exists():
        with open(h, encoding="utf-8", errors="replace") as f:
            if f.readline().startswith("# helestron-texto 2"):
                return Path(h)
    return pasta_proc(trab, d) / "texto.txt"


def _outline(pdf_path):
    """Marcadores do PDF (e-SAJ: '<tipo> (fls. A-B) - <data>'): {página (0-based): título}."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return {}
    try:
        r = PdfReader(pdf_path)
        marcas = {}

        def andar(itens):
            for it in itens:
                if isinstance(it, list):
                    andar(it)
                else:
                    try:
                        marcas.setdefault(r.get_destination_page_number(it), str(it.title).strip())
                    except Exception:
                        pass
        andar(r.outline)
        return marcas
    except Exception:
        return {}


def _paginas_pdf(arq: str) -> list:
    """Texto por página: pdfplumber (descarta a tarja vertical de assinatura) → pypdf → PyMuPDF → pdftotext."""
    try:
        import pdfplumber
        with pdfplumber.open(arq) as pdf:
            out = []
            for pg in pdf.pages:
                pg = pg.filter(lambda o: o.get("object_type") != "char" or o.get("upright", True))
                out.append(pg.extract_text() or "")
            return out
    except ImportError:
        pass
    try:
        from pypdf import PdfReader
        return [(pg.extract_text() or "") for pg in PdfReader(arq).pages]
    except ImportError:
        pass
    try:
        import fitz
        with fitz.open(arq) as doc:
            return [pg.get_text() for pg in doc]
    except ImportError:
        pass
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-layout", arq, "-"], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        return r.stdout.split("\f")[:-1] if r.stdout.endswith("\f") else r.stdout.split("\f")
    raise RuntimeError("nenhum extrator de PDF disponível (pdfplumber, pypdf, PyMuPDF ou pdftotext)")


def extrair(pdfs, destino: Path) -> dict:
    """Extração própria (sem o texto do Helestron), no mesmo formato de marcas. PDF do Helestron (nome
    = número CNJ): página N = folha N. Outro PDF: carimbo 'fls. N' da página se houver em mais da
    metade delas; senão, paginação não garantida (cite pelo documento)."""
    paginas, total = [], 0
    for arq in pdfs:
        marcas = _outline(arq)
        doc_atual = None
        textos = _paginas_pdf(arq)
        for i, t in enumerate(textos):
            t = (t or "").strip()
            doc_atual = marcas.get(i, doc_atual)
            linhas = t.splitlines()
            carimbo = re.search(r"\bfls\.\s*(\d{1,5})\b", "\n".join(linhas[:3] + linhas[-3:]))
            paginas.append({"t": t, "doc": doc_atual, "carimbo": int(carimbo.group(1)) if carimbo else None,
                            "pos": total + i + 1})
        total += len(textos)
    helestron = len(pdfs) == 1 and comum.numero_cnj(Path(pdfs[0]).stem) is not None
    carimbados = [p for p in paginas if p["carimbo"]]
    if len(carimbados) > len(paginas) / 2:  # o carimbo "fls. N" da margem prevalece sobre a posição no PDF
        modo = "folhas" if all(p["carimbo"] == p["pos"] for p in carimbados) else "carimbo"
    else:
        modo = "folhas" if helestron else "nao_garantida"
    linhas = [f"# texto-vara17 1 | paginacao={modo} | paginas={len(paginas)} | fonte=extracao propria"]
    sem_texto = []
    for p in paginas:
        if modo == "folhas":
            marca = f"=== [fl. {p['pos']}] ==="
        elif modo == "carimbo" and p["carimbo"]:
            marca = f"=== [fl. {p['carimbo']}] ==="
        else:
            marca = f"=== [pág. {p['pos']} do PDF] ==="
        linhas.append(marca)
        if p["doc"]:
            linhas.append(f"[documento: {p['doc']}]")
        if len(re.sub(r"fls\.\s*\d+", "", p["t"]).strip()) < 15:
            linhas.append(f"[página sem texto extraível — ver a página {p['pos']} do PDF]")
            sem_texto.append(p["pos"])
        else:
            linhas.append("\n".join(("· " + x) if x.startswith("=== [") else x for x in p["t"].splitlines()))
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return {"paginacao": modo, "paginas": len(paginas), "sem_texto": sem_texto}


def paginas_do_texto(arq: Path):
    """Itera (marca, documento, linhas) por página."""
    if not Path(arq).exists():
        sys.exit("Texto do processo ainda não extraído: rode `autos.py preparar N` antes.")
    marca, doc, buf = None, None, []
    with open(arq, encoding="utf-8", errors="replace") as f:
        for linha in f:
            linha = linha.rstrip("\n")
            m = MARCA.match(linha)
            if m:
                if marca is not None:
                    yield marca, doc, buf
                marca, buf = m.group(1), []
                continue
            if marca is None:
                continue
            d = DOC.match(linha)
            if d:
                doc = d.group(1)
                continue
            buf.append(linha)
    if marca is not None:
        yield marca, doc, buf


def _num_marca(marca: str):
    m = re.match(r"fls?\.\s*(\d+)", marca)
    return int(m.group(1)) if m else None


def construir_mapa(arq: Path) -> dict:
    pecas, sem_texto, ausentes, total = [], [], [], 0
    pistas = {k: [] for k in PISTAS}
    compiladas = {k: re.compile(v, re.I) for k, v in PISTAS.items()}
    for marca, doc, buf in paginas_do_texto(arq):
        total += 1
        corpo = "\n".join(buf)
        if any(SEM_TEXTO.match(x) for x in buf[:2]):
            sem_texto.append(marca)
        a = next((AUSENTE.match(x) for x in buf[:2] if AUSENTE.match(x)), None)
        if a:
            ausentes.append(f"{marca} ({a.group(1)})")
        nome = doc or "(sem marcador)"
        if pecas and pecas[-1]["doc"] == nome:
            pecas[-1]["ate"] = marca
        else:
            pecas.append({"doc": nome, "de": marca, "ate": marca})
        for k, rx in compiladas.items():
            if len(pistas[k]) < 8 and rx.search(corpo):
                pistas[k].append(marca)
    with open(arq, encoding="utf-8", errors="replace") as f:
        cab = f.readline().strip()
    return {"cabecalho": cab, "paginas": total, "pecas": pecas, "sem_texto": sem_texto,
            "ausentes": ausentes, "pistas": {k: v for k, v in pistas.items() if v}}


def _intervalo(pe):
    return pe["de"] if pe["de"] == pe["ate"] else f"{pe['de']} a {pe['ate']}"


def imprimir_mapa(n: str, mapa: dict, transcricoes=None, limite_pecas=70):
    print(f"MAPA {n} — {mapa['cabecalho']} — {mapa['paginas']} páginas")
    pecas = mapa["pecas"]
    if len(pecas) > limite_pecas:  # início (inicial, contestação) e fim (últimas manifestações)
        pecas = pecas[:25] + [{"doc": f"… {len(pecas) - 50} peças omitidas (mapa.json) …", "de": "", "ate": ""}] + pecas[-25:]
    for pe in pecas:
        print(f"- {pe['doc']}: {_intervalo(pe)}" if pe["de"] else f"- {pe['doc']}")
    if mapa["sem_texto"]:
        extra = len(mapa["sem_texto"]) - 40
        print(f"sem texto ({len(mapa['sem_texto'])}): " + ", ".join(mapa["sem_texto"][:40])
              + (f" … (+{extra} em mapa.json)" if extra > 0 else ""))
    if mapa["ausentes"]:
        print("folhas não disponíveis: " + "; ".join(mapa["ausentes"][:20]))
    for k, v in mapa["pistas"].items():
        print(f"pista {k}: " + ", ".join(v))
    for i, t in enumerate(transcricoes or [], 1):
        print(f"transcrição {i}: {t['data']} | {Path(t['arquivo']).name} ({t['tipo']}, {t['tamanho']} bytes)")


def preparar(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    lote_nums = lote_corrente(est)["numeros"]
    numeros = argv or com_apoio(est, lote_nums)
    via_helestron_feito = set()
    for x in numeros:
        p = proc(est, x)
        if p.get("sigiloso") and not autorizado(est, p["numero"]):
            print(f"{p.get('posicao', '?'):>2}. (processo sigiloso) — aguardando autorização")
            continue
        if p.get("sigiloso") and not p.get("ref"):
            print(f"{p.get('posicao', '?'):>2}. (processo sigiloso) — pasta somente leitura: não pode ser trabalhado")
            continue
        d = dados(est, p)
        n = d["numero"]
        arq = arquivo_texto(trab, p, d)
        if not arq.exists() and not p.get("sigiloso") and ph.python_helestron():
            pasta_pdf = str(Path(d["pdfs"][0]).parent)
            if pasta_pdf not in via_helestron_feito:  # o próprio Helestron extrai, sem baixar nada
                via_helestron_feito.add(pasta_pdf)
                ph.preparar(pasta_pdf)
            novo = _achar(Path(pasta_pdf), Path(d["pdfs"][0]).stem, n.split("-")[0], ".txt")
            if novo:
                p["texto_helestron"] = str(novo)
                arq = arquivo_texto(trab, p, {**d, "texto_helestron": str(novo)})
        if not arq.exists():
            try:
                extrair(d["pdfs"], arq)
            except Exception as e:  # registra e segue: falha de um processo não trava o lote
                p["etapa"] = "falhou"
                p["alerta"] = f"extração do texto falhou: {e}"
                print(f"{p.get('posicao', '?'):>2}. {n} — FALHOU na extração ({e})")
                continue
        mapa = construir_mapa(arq)
        comum.gravar_json(pasta_proc(trab, d) / "mapa.json", mapa)
        if not p.get("classe"):
            with open(arq, encoding="utf-8", errors="replace") as f:
                p["classe"] = _classe_do_texto(" ".join(pe["doc"] for pe in mapa["pecas"]) + f.read(20000))
        p["texto_ok"] = True
        if p["etapa"] == "pendente":
            p["etapa"] = "preparado"
        rotulo = "(processo sigiloso, autorizado)" if p.get("sigiloso") else n
        if not argv and n not in lote_nums:
            rotulo += " (apoio)"
        print(f"{p.get('posicao', '?'):>2}. {rotulo} | {p.get('classe') or '?'} | {mapa['paginas']} pág. | "
              f"{len(mapa['pecas'])} peças | sem texto: {len(mapa['sem_texto'])}"
              + (" | PAGINAÇÃO NÃO GARANTIDA" if "nao_garantida" in mapa["cabecalho"] else "")
              + (" | texto do Helestron" if "helestron-texto" in mapa["cabecalho"] else " | extração própria")
              + (f" | {len(d.get('transcricoes') or [])} transcrição(ões)" if d.get("transcricoes") else ""))
    salvar_estado(trab, est)
    return 0


def mapa_cmd(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    d = dados(est, proc(est, argv[0]))
    m = comum.ler_json(pasta_proc(trab, d) / "mapa.json")
    if not m:
        sys.exit("Rode antes `autos.py preparar`.")
    imprimir_mapa(d["numero"], m, d.get("transcricoes"))
    return 0


def capa_cmd(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    p = dados(est, proc(est, argv[0]))
    if not p.get("capa"):
        print("Sem capa do Helestron: use o mapa e as primeiras folhas (autuação).")
        return 0
    txt = Path(p["capa"]).with_suffix(".txt")
    if txt.exists():
        linhas = txt.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        print("\n".join(linhas[:120]) + (f"\n… ({len(linhas) - 120} linhas omitidas)" if len(linhas) > 120 else ""))
        return 0
    d = json.loads(Path(p["capa"]).read_text(encoding="utf-8-sig"))
    print(json.dumps({k: d.get(k) for k in ("capa", "partes", "marcas", "incidentes", "apensos", "audiencias",
                                             "justica_gratuita", "prioridade")}, ensure_ascii=False)[:6000])
    for mv in (d.get("movimentacoes") or [])[:30]:
        print("mov: " + json.dumps(mv, ensure_ascii=False)[:200])
    return 0


def _faixa(texto):
    a, _, b = texto.partition("-")
    return int(a), int(b or a)


def ler(argv):
    trab = comum.pasta_trabalho(argv)
    maximo = int(comum.arg(argv, "--max", 40000))
    fls = comum.arg(argv, "--fls")
    peca = comum.arg(argv, "--peca")
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    arq = arquivo_texto(trab, p, dados(est, p))
    saida = []
    ini, fim = _faixa(fls) if fls else (None, None)
    rx = re.compile(peca, re.I) if peca else None
    for marca, doc, buf in paginas_do_texto(arq):
        num = _num_marca(marca)
        if fls and (num is None or not ini <= num <= fim):
            continue
        if rx and not (doc and rx.search(doc)):
            continue
        saida.append(f"=== [{marca}] ===" + (f" [{doc}]" if doc else "") + "\n" + "\n".join(buf).strip())
    texto = "\n".join(saida)
    if not texto:
        print("Nada encontrado para o filtro (confira o mapa).")
        return 1
    if len(texto) > maximo:
        corte = texto[:maximo]
        ultima = re.findall(r"=== \[(.+?)\] ===", corte)
        print(corte + f"\n… [corte em {maximo} caracteres; continue a partir de {ultima[-1] if ultima else 'o ponto acima'}]")
    else:
        print(texto)
    return 0


def buscar(argv):
    trab = comum.pasta_trabalho(argv)
    ctx = int(comum.arg(argv, "--contexto", 250))
    maximo = int(comum.arg(argv, "--max", 30))
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    rx = re.compile(argv[1], re.I)
    arq = arquivo_texto(trab, p, dados(est, p))
    achados = 0
    for marca, doc, buf in paginas_do_texto(arq):
        corpo = re.sub(r"\s+", " ", " ".join(buf))
        for m in rx.finditer(corpo):
            a, b = max(0, m.start() - ctx), min(len(corpo), m.end() + ctx)
            print(f"[{marca}]" + (f" [{doc}]" if doc else "") + f" …{corpo[a:b]}…")
            achados += 1
            if achados >= maximo:
                print(f"(limite de {maximo} ocorrências; refine a expressão)")
                return 0
    if not achados:
        print("Nenhuma ocorrência.")
    return 0


def transcricoes(argv):
    """Transcrições de audiência do processo (pasta de transcrições do Helestron)."""
    trab = comum.pasta_trabalho(argv)
    maximo = int(comum.arg(argv, "--max", 60000))
    qual = comum.arg(argv, "--ler")
    est = carregar_estado(trab)
    d = dados(est, proc(est, argv[0]))
    lst = d.get("transcricoes") or []
    if not lst:
        print("Nenhuma transcrição associada a este processo"
              + ("" if est.get("pasta_transcricoes") else " (pasta de transcrições não localizada: informe-a no "
                 "inventário com --transcricoes)") + ".")
        return 0
    if qual is None:
        for i, t in enumerate(lst, 1):
            print(f"{i}. {t['data']} | {t['arquivo']} ({t['tipo']}, {t['tamanho']} bytes)")
        print("Leia com: autos.py transcricoes N --ler <i>. Transcrição automática: trecho decisivo vai à minuta "
              "com [Conferir com a gravação] em vermelho.")
        return 0
    t = lst[int(qual) - 1]
    texto = ph.texto_transcricao(t["arquivo"])
    print(f"### Transcrição {qual} — {t['data']} — {Path(t['arquivo']).name}")
    print(texto[:maximo] + (f"\n… [corte em {maximo} caracteres]" if len(texto) > maximo else ""))
    return 0


REQUISITOS_CS = [
    ("título: sentença ou acórdão", r"^(?:Senten[çc]a|Ac[óo]rd[ãa]o)\b|julgo (?:parcialmente )?(?:im)?procedente|"
                                    r"Vistos, relatados e discutidos|\bACORDAM\b"),
    ("trânsito em julgado", r"tr[âa]nsito em julgado|transitou|certid[ãa]o de tr[âa]nsito"),
    ("planilha ou memória de cálculo", r"planilha|mem[óo]ria de c[áa]lculo|demonstrativo (?:discriminado )?de c[áa]lculo|ProjefWeb"),
    ("índices de correção e juros (termos inicial e final)", r"IPCA-?E?|\bINPC\b|\bSELIC\b|poupan[çc]a|juros de mora|corre[çc][ãa]o monet"),
    ("fichas financeiras / contracheques", r"fichas? financeiras?|contracheques?|holerites?|demonstrativo de pagamento"),
    ("descontos: contribuição previdenciária", r"contribui[çc][ãa]o previdenci[áa]ria|desconto previdenci|PSSS|al[ií]quota previdenci"),
    ("descontos: imposto de renda / RRA", r"imposto de renda|\bIRRF?\b|\bRRA\b|rendimentos recebidos acumuladamente"),
    ("descontos: FGTS e outras contribuições", r"\bFGTS\b|Fundo de Garantia"),
    ("conta bancária do credor e do advogado", r"conta banc[áa]ria|conta corrente|\bag[êe]ncia\b|chave PIX|dados banc[áa]rios"),
    ("contrato de honorários (destaque)", r"contrato de (?:presta[çc][ãa]o de servi[çc]os|honor[áa]rios)|destaque (?:dos|de) honor"),
    ("óbito, espólio, inventário e herdeiros", r"[óo]bito|falecid[oa]|esp[óo]lio|invent[áa]rio|inventariante|herdeir|formal de partilha|escritura p[úu]blica|vi[úu]v[oa]|c[ôo]njuge"),
    ("impugnação da Fazenda (art. 535)", r"impugna[çc][ãa]o ao cumprimento|impugna[çc][ãa]o [àa] execu|excesso de execu[çc][ãa]o|art\.?\s*535"),
    ("requisitório (RPV ou precatório)", r"\bRPV\b|requisi[çc][ãa]o de pequeno valor|precat[óo]rio|requisit[óo]rio"),
    ("cessão de crédito", r"cess[ãa]o de cr[ée]dito|cession[áa]ri"),
    ("pagamento, alvará e levantamento", r"alvar[áa]|levantamento|comprovante de pagamento|dep[óo]sito judicial"),
]


def relacionados_cmd(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    d = dados(est, p)
    rel = relacionados(est, d["numero"])
    if not rel:
        print("Sem autos relacionados na pasta" + (f" — os autos de origem ({base_cnj(d['numero'])}) não foram baixados: "
              "peça ao usuário que os baixe pelo Helestron." if len(d["numero"]) > 25 else "."))
        return 0
    for n in rel:
        q = est["processos"][n]
        print(f"{n} | {q.get('classe') or '?'} | texto: {arquivo_texto(trab, q, q).as_posix()}"
              + ("" if arquivo_texto(trab, q, q).exists() else " (rode `autos.py preparar`)"))
    return 0


def requisitos(argv):
    """Pistas, com as fls., de cada requisito do cumprimento de sentença — no processo e nos relacionados.
    Pista não é prova: confirme lendo as fls. indicadas."""
    trab = comum.pasta_trabalho(argv)
    maximo = int(comum.arg(argv, "--max", 6))
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    d = dados(est, p)
    alvos = [(d["numero"], arquivo_texto(trab, p, d))]
    for n in relacionados(est, d["numero"]):
        q = est["processos"][n]
        alvos.append((n, arquivo_texto(trab, q, q)))
    compiladas = [(nome, re.compile(rx, re.I)) for nome, rx in REQUISITOS_CS]
    achados = {nome: [] for nome, _ in REQUISITOS_CS}
    for n, arq in alvos:
        if not arq.exists():
            print(f"(texto de {n} ainda não extraído: rode `autos.py preparar {n}`)")
            continue
        rotulo = "" if n == d["numero"] else f"{n} "
        for marca, doc, buf in paginas_do_texto(arq):
            corpo = (doc or "") + " " + " ".join(buf)  # o marcador da peça também é pista (v.g., "Sentença")
            for nome, rx in compiladas:
                if len(achados[nome]) < maximo and rx.search(corpo):
                    achados[nome].append(f"{rotulo}{marca}" + (f" [{doc[:40]}]" if doc else ""))
    print(f"REQUISITOS — {d['numero']} (pistas por palavra-chave; confirme lendo as fls.)")
    for nome, lst in achados.items():
        print(f"- {nome}: " + ("; ".join(lst) if lst else "NÃO LOCALIZADO"))
    if len(d["numero"]) > 25 and base_cnj(d["numero"]) not in est["processos"]:
        print(f"! autos de origem {base_cnj(d['numero'])} ausentes da pasta: o título não foi conferido")
    return 0


# ---------------------------------------------------------------- controle do lote

def caminhos(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    d = dados(est, p)
    base = pasta_proc(trab, d)
    base.mkdir(parents=True, exist_ok=True)
    print(json.dumps({"numero": d["numero"], "classe": p.get("classe"),
                      "texto": arquivo_texto(trab, p, d).as_posix(), "pasta_processo": base.as_posix(),
                      "dossie": (base / "dossie.json").as_posix(), "calculos": (base / "calculos.json").as_posix(),
                      "minuta_txt": (base / "minuta.txt").as_posix(), "saida": pasta_minutas(est, p).as_posix(),
                      "ledger": (trab / "verificacoes").as_posix(),
                      "transcricoes": [Path(t["arquivo"]).as_posix() for t in d.get("transcricoes") or []],
                      "trabalho": trab.as_posix()}, ensure_ascii=False, indent=1))
    return 0


def autorizar(argv):
    trab = comum.pasta_trabalho(argv)
    ordem = comum.arg(argv, "--ordem")
    if not ordem:
        sys.exit("Informe --ordem com o texto literal da autorização dada pelo magistrado no chat.")
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    est.setdefault("autorizados", {})[p["numero"]] = {"data": comum.hoje(), "ordem": ordem}
    salvar_estado(trab, est)
    print(f"Posição {p.get('posicao', '?')}: sigiloso autorizado hoje ({comum.hoje()}).")
    return 0


def marcar(argv):
    trab = comum.pasta_trabalho(argv)
    campos = {k: comum.arg(argv, f"--{k}") for k in ("ato", "resultado", "alerta", "minuta", "justificativa")}
    est = carregar_estado(trab)
    p = proc(est, argv[0])
    etapa = argv[1]
    if etapa not in ETAPAS:
        sys.exit(f"Etapa inválida: {etapa}. Use: {', '.join(ETAPAS)}")
    p["etapa"] = etapa
    p.setdefault("historico", []).append(f"{datetime.now().isoformat(timespec='minutes')} {etapa}")
    def juntar(destino: dict):
        for k, v in campos.items():
            if not v:
                continue
            if k in ("alerta", "justificativa") and destino.get(k) and v not in destino[k]:
                destino[k] = destino[k] + " | " + v  # um registro por apontamento, sem sobrescrever
            else:
                destino[k] = v

    if p.get("ref"):
        guarda_sigilo(est, p)
        reais = comum.ler_json(p["ref"], {})
        juntar(reais.setdefault(p["numero"], {}))
        comum.gravar_json(p["ref"], reais)
    else:
        juntar(p)
    salvar_estado(trab, est)
    print(f"posição {p.get('posicao')}: {etapa}")
    return 0


def _linha(est, n):
    p = est["processos"][n]
    if p.get("sigiloso"):
        situacao = p["etapa"] if autorizado(est, n) else "aguardando autorização"
        return f"| {p.get('posicao')} | (processo sigiloso) | — | {situacao} | ver pasta dos sigilosos | — |"
    return (f"| {p.get('posicao')} | {n} | {p.get('classe') or '?'} | {p['etapa']} | {p.get('ato') or '—'} | "
            f"{p.get('resultado') or '—'} |")


def status(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    lote = lote_corrente(est)
    print(f"LOTE {lote['id']}")
    print("| # | processo | classe | etapa | ato | resultado |\n|---|---|---|---|---|---|")
    for n in lote["numeros"]:
        print(_linha(est, n))
    return 0


def relatorio(argv):
    trab = comum.pasta_trabalho(argv)
    est = carregar_estado(trab)
    lote = lote_corrente(est)
    destino = Path(est["minutas"]) / lote["id"] / "LISTA_TRABALHO.md"
    out = [f"# Lote {lote['id']} — 17ª Vara Cível da Capital", "",
           "Minutas de apoio elaboradas com auxílio de inteligência artificial, sujeitas à revisão, à alteração "
           "e à decisão do magistrado (art. 93, IX, da CF; Resolução CNJ n.º 615/2025). Uso interno.", "",
           "| # | processo | classe | etapa | ato | resultado |", "|---|---|---|---|---|---|"]
    out += [_linha(est, n) for n in lote["numeros"]]
    if lote.get("nao_encontrados"):
        out += ["", "Não encontrados na pasta do Helestron: " + ", ".join(lote["nao_encontrados"])]
    publicos = [n for n in lote["numeros"] if not est["processos"][n].get("sigiloso")]
    for titulo, campo in (("Alertas e pendências", "alerta"),
                          ("Apontamentos do portão mantidos (justificativa)", "justificativa")):
        itens = [(n, est["processos"][n].get(campo)) for n in publicos if est["processos"][n].get(campo)]
        if itens:
            out += ["", f"## {titulo}", ""] + [f"- {n}: {a}" for n, a in itens]
    out += ["", "## Minutas em Word (.docx)", ""]
    for n in publicos:
        arquivos = sorted(f.name for f in destino.parent.glob(f"Minuta_{n}_*.docx"))
        if arquivos:
            out.append(f"- {n}: " + "; ".join(arquivos))
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(destino)
    return 0


def validar(argv):
    falhou = False
    for x in argv:
        n = comum.completar_cnj(x) or x
        r = comum.validar_cnj(n)
        falhou |= not r["valido"]
        print(json.dumps(r, ensure_ascii=False))
    return 1 if falhou else 0


COMANDOS = {"inventario": inventario, "preparar": preparar, "caminhos": caminhos, "mapa": mapa_cmd,
            "capa": capa_cmd, "ler": ler, "buscar": buscar, "transcricoes": transcricoes, "autorizar": autorizar,
            "marcar": marcar, "status": status, "relatorio": relatorio, "validar": validar,
            "requisitos": requisitos, "relacionados": relacionados_cmd}


def main(argv):
    comum.utf8_console()
    if not argv or argv[0] not in COMANDOS or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 2
    return COMANDOS[argv[0]](argv[1:]) or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
