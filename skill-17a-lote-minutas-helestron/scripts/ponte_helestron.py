#!/usr/bin/env python3
"""Ponte com o aplicativo Helestron: pasta de downloads (acervo), sigilosos e transcrições de audiências.

A skill NÃO baixa processos nem acessa o e-SAJ: usa o que o Helestron já gravou. Tudo aqui é
leitura; a única chamada que grava é `preparar` (o próprio Helestron extrai o texto dos PDFs que
já baixou, na pasta `_texto` dele), e só para pastas que não sejam de sigilosos.

Uso:
  python -I ponte_helestron.py diagnostico [--downloads <pasta>] [--transcricoes <pasta>]
        JSON com o Python do Helestron, a versão, o acervo, a pasta de sigilosos, a pasta de
        transcrições e o que falta. Não expõe senha, perfil nem sessão (o `caminhos --json` do
        programa não os contém).
  python -I ponte_helestron.py transcricoes [--transcricoes <pasta>] [--numero N]
        Índice das transcrições de audiências por processo (número CNJ no nome ou no início do
        arquivo).
  python -I ponte_helestron.py ler-transcricao <arquivo> [--max 60000]
        Texto da transcrição (txt, md, docx, srt, vtt ou json), com as marcas de tempo.

(O arquivo não se chama helestron.py de propósito: o nome ocultaria o pacote do próprio programa.)

Localização do programa (nessa ordem): variável HELESTRON_PYTHON; o próprio interpretador, se
importar `helestron`; registro HKCU\\Software\\Helestron (valor Python); %LOCALAPPDATA%\\Programs\\
Helestron\\python.exe; registro de desinstalação (InstallLocation).
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
sys.dont_write_bytecode = True
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402

EXT_TRANSCRICAO = {".txt", ".md", ".docx", ".srt", ".vtt", ".json"}
NOMES_TRANSCRICAO = ("Transcrições", "Transcricoes", "transcricoes", "_transcricoes", "Transcrições de audiências",
                     "Transcricoes de audiencias", "Audiências", "Audiencias", "audiencias", "_audiencias")
_CACHE = {}


# ------------------------------------------------------------------ programa

def _registro(chave: str, valor: str):
    try:
        import winreg
    except ImportError:
        return None
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, chave) as k:
            return winreg.QueryValueEx(k, valor)[0]
    except OSError:
        return None


def python_helestron():
    """Caminho do Python do Helestron, ou None (Cowork, nuvem, programa ausente)."""
    if "python" in _CACHE:
        return _CACHE["python"]
    candidatos = [os.environ.get("HELESTRON_PYTHON")]
    if importlib.util.find_spec("helestron") is not None:
        candidatos.append(sys.executable)
    candidatos.append(_registro(r"Software\Helestron", "Python"))
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidatos.append(str(Path(local) / "Programs" / "Helestron" / "python.exe"))
    inst = _registro(r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Helestron", "InstallLocation")
    if inst:
        candidatos.append(str(Path(inst) / "python.exe"))
    achado = next((c for c in candidatos if c and Path(c).is_file()), None)
    _CACHE["python"] = achado
    return achado


def _rodar(args, timeout=120):
    py = python_helestron()
    if not py:
        return None, "Helestron não encontrado neste computador"
    try:
        r = subprocess.run([py, "-I", "-X", "utf8", "-m", "helestron", *args], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        return None, f"falha ao executar o Helestron: {e}"
    saida = (r.stdout or "").strip()
    inicio = saida.find("{")
    if inicio < 0:
        return None, (r.stderr or saida or f"código {r.returncode}").strip()[:400]
    try:
        return json.loads(saida[inicio:]), None
    except ValueError:
        return None, "saída do Helestron não é JSON"


def caminhos() -> dict:
    """`helestron caminhos --json` (versão 1.0.2 ou superior). {} se indisponível."""
    if "caminhos" not in _CACHE:
        dados, erro = _rodar(["caminhos", "--json"], timeout=60)
        _CACHE["caminhos"] = dados or ({"_erro": erro} if erro else {})
    return _CACHE["caminhos"]


def preparar(pasta) -> dict:
    """Extração do texto pelo próprio Helestron (`preparar --pasta`), sem baixar nada."""
    if "sigilos" in str(pasta).lower():
        return {"_erro": "pasta de sigilosos: a extração só se faz com autorização (autos.py autorizar)"}
    dados, erro = _rodar(["preparar", "--pasta", str(pasta), "--json"], timeout=1800)
    return dados or {"_erro": erro}


# ------------------------------------------------------------------ pastas

def _dir(valor):
    if not valor:
        return None
    p = Path(str(valor)).expanduser()
    return p.resolve() if p.is_dir() else None


def pasta_downloads(informada=None):
    cfg = comum.config()["pastas"]
    for valor in (informada, cfg.get("downloads"), caminhos().get("acervo")):
        p = _dir(valor)
        if p:
            return p
    return None


def pasta_sigilosos():
    return _dir(caminhos().get("sigilosos"))


def pasta_transcricoes(informada=None, downloads=None):
    """Pasta das transcrições de audiências feitas pelo Helestron (ou None)."""
    cfg = comum.config()["pastas"]
    for valor in (informada, cfg.get("transcricoes")):
        p = _dir(valor)
        if p:
            return p
    for chave, valor in caminhos().items():
        if isinstance(valor, str) and re.search(r"transcri|audienc", chave, re.I):
            p = _dir(valor)
            if p:
                return p
    bases = []
    for b in (downloads, pasta_downloads()):
        if b:
            bases += [Path(b), Path(b).parent]
    for base in bases:
        for nome in NOMES_TRANSCRICAO:
            p = _dir(base / nome)
            if p:
                return p
    for base in bases:  # dois níveis, com teto: pastas cujo nome fale de transcrição ou audiência
        try:
            for filho in list(base.iterdir())[:400]:
                if filho.is_dir() and re.search(r"transcri|audi[eê]nc", filho.name, re.I):
                    return filho.resolve()
        except OSError:
            continue
    return None


# ------------------------------------------------------------------ transcrições

def _texto_docx(arq: Path) -> str:
    with zipfile.ZipFile(arq) as z:
        xml = z.read("word/document.xml").decode("utf-8", "replace")
    pars = []
    for p in re.findall(r"<w:p[ >].*?</w:p>", xml, re.S):
        t = "".join(re.findall(r"<w:t(?: [^>]*)?>([^<]*)</w:t>", p))
        pars.append(t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"'))
    return "\n".join(pars)


def _hms(seg) -> str:
    try:
        s = float(seg)
    except (TypeError, ValueError):
        return str(seg)
    h, r = divmod(int(s), 3600)
    m, s2 = divmod(r, 60)
    return f"{h:02d}:{m:02d}:{s2:02d}" if h else f"{m:02d}:{s2:02d}"


def _texto_json(dados) -> str:
    """JSON de transcrição em formato desconhecido: procura a lista de segmentos e os campos usuais."""
    segs = None
    if isinstance(dados, list):
        segs = dados
    elif isinstance(dados, dict):
        for k in ("segmentos", "segments", "falas", "trechos", "utterances", "transcricao", "transcription", "itens"):
            if isinstance(dados.get(k), list):
                segs = dados[k]
                break
        if segs is None:
            for k in ("texto", "text", "transcricao", "transcription"):
                if isinstance(dados.get(k), str):
                    return dados[k]
    if not segs:
        return json.dumps(dados, ensure_ascii=False, indent=1)
    linhas = []
    for s in segs:
        if not isinstance(s, dict):
            linhas.append(str(s))
            continue
        t = next((s[k] for k in ("texto", "text", "fala", "conteudo") if isinstance(s.get(k), str)), "")
        ini = next((s[k] for k in ("inicio", "start", "begin", "tempo", "time") if k in s), None)
        quem = next((s[k] for k in ("falante", "speaker", "locutor", "orador", "participante") if s.get(k)), None)
        linhas.append((f"[{_hms(ini)}] " if ini is not None else "") + (f"{quem}: " if quem else "") + t.strip())
    return "\n".join(linhas)


def _texto_legenda(bruto: str) -> str:
    linhas, tempo = [], None
    for ln in bruto.splitlines():
        ln = ln.strip()
        m = re.match(r"(\d{1,2}:)?(\d{2}):(\d{2})[.,]\d{3}\s*-->", ln)
        if m:
            h = int((m.group(1) or "0:")[:-1])
            tempo = f"{h:02d}:{m.group(2)}:{m.group(3)}" if h else f"{m.group(2)}:{m.group(3)}"
            continue
        if not ln or ln.isdigit() or ln.upper().startswith("WEBVTT") or ln.startswith("NOTE"):
            continue
        linhas.append(f"[{tempo}] {ln}" if tempo else ln)
        tempo = None
    return "\n".join(linhas)


def texto_transcricao(arq) -> str:
    arq = Path(arq)
    ext = arq.suffix.lower()
    if ext == ".docx":
        return _texto_docx(arq)
    bruto = arq.read_text(encoding="utf-8-sig", errors="replace")
    if ext in (".srt", ".vtt"):
        return _texto_legenda(bruto)
    if ext == ".json":
        try:
            return _texto_json(json.loads(bruto))
        except ValueError:
            return bruto
    return bruto


def _data_no_nome(nome: str):
    """Data da audiência no nome do arquivo (aaaa-mm-dd ou dd-mm-aaaa), fora do número CNJ."""
    nome = comum.CNJ_RE.sub(" ", nome)
    m = re.search(r"(?<!\d)((?:19|20)\d{2})[-_.](0[1-9]|1[0-2])[-_.](0[1-9]|[12]\d|3[01])(?!\d)", nome)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"(?<!\d)(0[1-9]|[12]\d|3[01])[-_.](0[1-9]|1[0-2])[-_.]((?:19|20)\d{2})(?!\d)", nome)
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    return None


def indexar_transcricoes(pasta, limite=8000) -> dict:
    """{numero CNJ: [ {arquivo, tipo, data, tamanho, sigilosa} ]} — número no nome do arquivo, no
    nome da pasta ou nas primeiras linhas do conteúdo."""
    indice, vistos = {}, 0
    pasta = Path(pasta)
    for raiz, dirs, arqs in os.walk(pasta):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        r = Path(raiz)
        for a in arqs:
            arq = r / a
            if arq.suffix.lower() not in EXT_TRANSCRICAO:
                continue
            vistos += 1
            if vistos > limite:
                break
            n = comum.completar_cnj(a) or comum.completar_cnj(r.name)
            if not n:
                try:
                    amostra = texto_transcricao(arq)[:4000] if arq.suffix.lower() == ".docx" else \
                        arq.read_text(encoding="utf-8-sig", errors="replace")[:4000]
                except (OSError, zipfile.BadZipFile, KeyError):
                    continue
                n = comum.numero_cnj(amostra)
            if not n:
                continue
            try:
                st = arq.stat()
            except OSError:
                continue
            indice.setdefault(n, []).append({
                "arquivo": str(arq), "tipo": arq.suffix.lower().lstrip("."),
                "data": _data_no_nome(a) or datetime.fromtimestamp(st.st_mtime).date().isoformat(),
                "tamanho": st.st_size,
                "sigilosa": any("sigilos" in p.lower() for p in arq.relative_to(pasta).parts[:-1])})
    for lst in indice.values():
        lst.sort(key=lambda x: (x["data"], x["arquivo"]))
    return indice


# ------------------------------------------------------------------ comandos

def diagnostico(argv):
    downloads = pasta_downloads(comum.arg(argv, "--downloads"))
    transc = pasta_transcricoes(comum.arg(argv, "--transcricoes"), downloads)
    c = caminhos()
    recursos = c.get("recursos") or []
    out = {
        "python_helestron": python_helestron(),
        "versao": c.get("versao"),
        "caminhos_erro": c.get("_erro"),
        "downloads": str(downloads) if downloads else None,
        "sigilosos": str(pasta_sigilosos()) if pasta_sigilosos() else None,
        "transcricoes": str(transc) if transc else None,
        "separar_sigilosos": c.get("separar_sigilosos"),
        "preparar_disponivel": ("preparar.pasta" in recursos) if recursos else None,
        "chaves_caminhos": sorted(k for k in c if not k.startswith("_")),
    }
    falta = []
    if not downloads:
        falta.append("pasta de downloads: informe-a no chat (ou conecte-a, no Cowork)")
    if not transc:
        falta.append("pasta de transcrições não localizada: informe-a no chat se o lote tiver audiência")
    if c and c.get("separar_sigilosos") is False:
        falta.append("Helestron com 'Separar os processos sigilosos' desligado: sigilo só pela capa")
    out["pendencias"] = falta
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0 if downloads else 1


def transcricoes_cmd(argv):
    numero = comum.arg(argv, "--numero")
    pasta = pasta_transcricoes(comum.arg(argv, "--transcricoes"), pasta_downloads(comum.arg(argv, "--downloads")))
    if not pasta:
        print(json.dumps({"pasta": None, "aviso": "pasta de transcrições não localizada"}, ensure_ascii=False))
        return 1
    idx = indexar_transcricoes(pasta)
    if numero:
        n = comum.completar_cnj(numero)
        idx = {n: idx.get(n, [])}
    print(json.dumps({"pasta": str(pasta), "processos": len(idx), "indice": idx}, ensure_ascii=False, indent=1))
    return 0


def ler_transcricao(argv):
    maximo = int(comum.arg(argv, "--max", 60000))
    if not argv:
        sys.exit("Uso: ponte_helestron.py ler-transcricao <arquivo> [--max 60000]")
    texto = texto_transcricao(argv[0])
    print(texto[:maximo] + (f"\n… [corte em {maximo} caracteres]" if len(texto) > maximo else ""))
    return 0


COMANDOS = {"diagnostico": diagnostico, "transcricoes": transcricoes_cmd, "ler-transcricao": ler_transcricao}


def main(argv):
    comum.utf8_console()
    if not argv or argv[0] not in COMANDOS:
        print(__doc__)
        return 2
    return COMANDOS[argv[0]](argv[1:]) or 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
