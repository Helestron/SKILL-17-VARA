#!/usr/bin/env python3
"""Utilidades comuns aos scripts da skill (configuração, pasta de trabalho, JSON, número CNJ).

Só biblioteca padrão: os scripts rodam no Python do próprio Helestron (`python -I`) ou em qualquer
Python 3.9+. Nada se grava na pasta da skill (sem __pycache__).

Pasta de trabalho (estado, ledgers, texto, dossiês): `--trabalho <dir>` (ou `-t <dir>`) em qualquer
script; na falta, a variável de ambiente VARA17_TRABALHO; na falta, `./_Vara17/trabalho`, se existir.
`autos.py inventario` cria a pasta e imprime o caminho a usar nas chamadas seguintes.
"""
import json
import os
import re
import sys
sys.dont_write_bytecode = True
import unicodedata
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CONFIG = RAIZ / "config" / "vara.json"
CNJ_RE = re.compile(r"(\d{7})-?(\d{2})\.?(\d{4})\.?(\d)\.?(\d{2})\.?(\d{4})(?:[-/](\d{2}))?")
CNJ_ABREV_RE = re.compile(r"\b(\d{7})-(\d{2})\.(\d{4})(?![.\d])(?:[-/](\d{2}))?")


def utf8_console():
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8")
        except Exception:
            pass


def config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8-sig"))


def ler_json(caminho, padrao=None):
    p = Path(caminho)
    if not p.exists():
        return padrao
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return padrao


def gravar_json(caminho, dados):
    """Gravação atômica (arquivo temporário + troca): uma queda não corrompe o estado."""
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(p)


def nfc(texto: str) -> str:
    return unicodedata.normalize("NFC", texto or "")


def sem_acento(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn")


def hoje() -> str:
    return date.today().isoformat()


def arg(argv, nome, padrao=None):
    """Valor de `--nome valor` (ou do atalho) em argv; remove os dois itens da lista."""
    atalhos = {"--trabalho": "-t"}
    for chave in (nome, atalhos.get(nome)):
        if chave and chave in argv:
            i = argv.index(chave)
            valor = argv[i + 1] if i + 1 < len(argv) else padrao
            del argv[i:i + 2]
            return valor
    return padrao


def flag(argv, nome) -> bool:
    if nome in argv:
        argv.remove(nome)
        return True
    return False


def pasta_trabalho(argv, criar=False) -> Path:
    valor = arg(argv, "--trabalho") or os.environ.get("VARA17_TRABALHO")
    if not valor:
        candidato = Path.cwd() / "_Vara17" / "trabalho"
        if candidato.exists() or criar:
            valor = str(candidato)
    if not valor:
        sys.exit("Pasta de trabalho não definida: passe --trabalho <dir> (o caminho é impresso por "
                 "`autos.py inventario`).")
    p = Path(valor).expanduser().resolve()
    if criar:
        p.mkdir(parents=True, exist_ok=True)
    return p


# ------------------------------------------------------------------ número CNJ (Resolução CNJ n.º 65/2008)

def digito_cnj(seq: str, ano: str, j: str, tr: str, foro: str) -> str:
    return f"{98 - (int(f'{seq}{ano}{j}{tr}{foro}00') % 97):02d}"


def numero_cnj(texto: str):
    """Primeiro número CNJ completo do texto, normalizado (com o sufixo -NN do incidente, se houver)."""
    m = CNJ_RE.search(texto or "")
    if not m:
        return None
    seq, dd, ano, j, tr, foro, inc = m.groups()
    n = f"{seq}-{dd}.{ano}.{j}.{tr}.{foro}"
    return f"{n}-{inc}" if inc else n


def completar_cnj(texto: str, foro: str = None):
    """Aceita o número completo ou a forma abreviada NNNNNNN-DD.AAAA (completa com 8.02.<foro da vara>)."""
    n = numero_cnj(texto)
    if n:
        return n
    m = CNJ_ABREV_RE.search(texto or "")
    if not m:
        return None
    foro = foro or config()["unidade"]["foro_cnj"]
    base = f"{m.group(1)}-{m.group(2)}.{m.group(3)}.8.02.{foro}"
    return f"{base}-{m.group(4)}" if m.group(4) else base


def validar_cnj(numero: str) -> dict:
    m = CNJ_RE.fullmatch((numero or "").strip())
    if not m:
        return {"numero": numero, "valido": False, "motivo": "formato inválido"}
    seq, dd, ano, j, tr, foro, _ = m.groups()
    esperado = digito_cnj(seq, ano, j, tr, foro)
    r = {"numero": numero, "valido": dd == esperado and j == "8" and tr == "02", "foro": foro}
    if dd != esperado:
        r["motivo"] = f"dígito verificador não confere (esperado {esperado})"
    elif j != "8" or tr != "02":
        r["motivo"] = "não pertence ao TJAL (J.TR deveria ser 8.02)"
    elif foro != config()["unidade"]["foro_cnj"]:
        r["aviso"] = f"foro {foro}: processo de outra comarca — confira se é da 17ª Vara antes de minutar"
    return r


def extrair_numeros(texto: str) -> list:
    """Números CNJ (completos ou abreviados) do texto, normalizados e sem repetição, na ordem."""
    vistos = []
    for m in re.finditer(r"\d{7}-?\d{2}\.?\d{4}(?:\.?\d\.?\d{2}\.?\d{4})?(?:[-/]\d{2})?", texto or ""):
        n = completar_cnj(m.group(0))
        if n and n not in vistos:
            vistos.append(n)
    return vistos


def dominio_oficial(url: str, tipo: str) -> bool:
    """A fonte é oficial para o tipo de citação? (lei: Planalto/SAPL; jurisprudência: STF, STJ, TJAL;
    JusBrasil só como comprovação de autenticidade; ato normativo: CNJ/TJAL)."""
    cfg = config()["fontes_oficiais"]
    u = (url or "").lower()
    if tipo in ("dispositivo", "lei"):
        dominios = cfg["legislacao"]
    elif tipo == "ato_normativo":
        dominios = cfg["atos_normativos"] + cfg["legislacao"]
    else:
        dominios = cfg["jurisprudencia"] + cfg["autenticidade"]
    m = re.match(r"^(?:https?://)?([^/\s:]+)", u)
    host = m.group(1) if m else ""
    return any(host == d or host.endswith("." + d) for d in dominios)
