#!/usr/bin/env python3
"""Jurisprudência do STJ pelo Portal de Dados Abertos (dadosabertos.web.stj.jus.br) — via oficial
para consulta automatizada, sem CAPTCHA nem verificação anti-robô.

O portal publica, em CKAN, os "espelhos de acórdãos" de cada órgão julgador (Corte Especial,
Seções e Turmas) em arquivos JSON mensais: ementa, tese, relator, datas, classe, número, referências
legislativas e temas. Este script baixa os meses pedidos para um cache local e busca nele; o
resultado já vem no formato de entrada do ledger (`ledger.py add`).

Uso:
  python -I stj_dados_abertos.py conjuntos [--filtro espelhos]
  python -I stj_dados_abertos.py baixar --conjunto <id> [--desde AAAAMM] [--ate AAAAMM] [--cache <dir>]
  python -I stj_dados_abertos.py buscar "<termos>" [--conjunto <id>] [--classe REsp] [--max 15] [--cache <dir>]
  python -I stj_dados_abertos.py tema <número> [--cache <dir>]

Cache padrão: <pasta de trabalho>/stj_dados_abertos (ou ./_Vara17/stj_dados_abertos). O cache
persiste entre lotes: baixa-se cada mês uma vez. Os nomes dos campos variam entre versões do
portal; a busca lê qualquer campo de texto e o mapeamento para o ledger tenta os nomes usuais.

Requisições identificadas, uma por vez, com pausa entre elas — é uso que o portal prevê. Rotas e
nomes de conjunto conferidos na primeira execução vão para o caderno de bordo.
"""
import json
import os
import re
import sys
sys.dont_write_bytecode = True
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402

BASE = comum.config()["jurisprudencia_rotas"]["stj_dados_abertos"].rstrip("/")
UA = "Vara17-TJAL-minutas/2.0 (consulta a dados abertos; uso institucional)"
CAMPOS_TEXTO = ("ementa", "teseJuridica", "tese", "decisao", "termosAuxiliares", "tema", "notas",
                "informacoesComplementares", "referenciasLegislativas", "jurisprudenciaCitada")


def _cache(argv) -> Path:
    c = comum.arg(argv, "--cache")
    trab = comum.arg(argv, "--trabalho") or os.environ.get("VARA17_TRABALHO")
    if c:
        p = Path(c)
    elif trab:
        p = Path(trab) / "stj_dados_abertos"
    else:
        p = Path.cwd() / "_Vara17" / "stj_dados_abertos"
    p.mkdir(parents=True, exist_ok=True)
    return p


def _get(url: str, binario=False, tentativas=3):
    erro = None
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as r:
                dados = r.read()
            time.sleep(1.0)
            return dados if binario else json.loads(dados.decode("utf-8-sig"))
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            erro = e
            time.sleep(2 ** (i + 1))
    raise RuntimeError(f"falha ao acessar {url}: {erro}")


def _api(acao: str, **params):
    url = f"{BASE}/api/3/action/{acao}?" + urllib.parse.urlencode(params)
    r = _get(url)
    if not r.get("success"):
        raise RuntimeError(f"API do portal recusou {acao}: {r.get('error')}")
    return r["result"]


def conjuntos(argv):
    filtro = (comum.arg(argv, "--filtro") or "espelhos").lower()
    nomes = _api("package_list")
    out = [n for n in nomes if filtro in n.lower()]
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


def baixar(argv):
    cache = _cache(argv)
    conjunto = comum.arg(argv, "--conjunto")
    desde = comum.arg(argv, "--desde", "000000")
    ate = comum.arg(argv, "--ate", "999999")
    if not conjunto:
        sys.exit("Informe --conjunto (veja `conjuntos`).")
    pacote = _api("package_show", id=conjunto)
    destino = cache / conjunto
    destino.mkdir(parents=True, exist_ok=True)
    baixados, pulados = [], 0
    for rec in pacote.get("resources", []):
        url = rec.get("url") or ""
        nome = Path(urllib.parse.urlparse(url).path).name
        if not nome.lower().endswith(".json"):
            continue
        mes = re.search(r"(\d{6})", nome)
        if mes and not (desde <= mes.group(1) <= ate):
            continue
        alvo = destino / nome
        if alvo.exists() and alvo.stat().st_size > 0:
            pulados += 1
            continue
        alvo.write_bytes(_get(url, binario=True))
        (destino / (nome + ".url")).write_text(url, encoding="utf-8")
        baixados.append(nome)
    print(json.dumps({"conjunto": conjunto, "baixados": baixados, "ja_em_cache": pulados,
                      "pasta": str(destino)}, ensure_ascii=False, indent=1))
    return 0


def _registros(cache: Path, conjunto=None):
    pastas = [cache / conjunto] if conjunto else [p for p in cache.iterdir() if p.is_dir()]
    for pasta in pastas:
        for arq in sorted(pasta.glob("*.json")):
            try:
                dados = json.loads(arq.read_text(encoding="utf-8-sig"))
            except (OSError, ValueError):
                continue
            itens = dados if isinstance(dados, list) else dados.get("documentos") or dados.get("itens") or []
            url = (pasta / (arq.name + ".url"))
            fonte = url.read_text(encoding="utf-8").strip() if url.exists() else f"{BASE}/dataset/{pasta.name}"
            for it in itens:
                if isinstance(it, dict):
                    yield it, fonte, pasta.name


def _txt(v):
    if isinstance(v, (list, tuple)):
        return " ".join(_txt(x) for x in v)
    if isinstance(v, dict):
        return " ".join(_txt(x) for x in v.values())
    return str(v or "")


def _data(v):
    s = _txt(v)
    m = re.search(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m = re.search(r"\b(\d{4})(\d{2})(\d{2})\b", s)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}" if m else s.strip() or None


def _entrada(it, fonte, conjunto):
    pega = lambda *ks: next((it[k] for k in ks if it.get(k)), None)  # noqa: E731
    classe = _txt(pega("siglaClasse", "classe", "descricaoClasse")).strip()
    numero = _txt(pega("numeroProcesso", "numero", "processo")).strip()
    chave = f"{classe} {numero}".strip()
    return {
        "tipo": "precedente", "chave": chave, "tribunal": "STJ",
        "orgao": _txt(pega("nomeOrgaoJulgador", "orgaoJulgador")).strip() or conjunto,
        "relator": _txt(pega("ministroRelator", "relator")).strip(),
        "julgamento": _data(pega("dataDecisao", "dataJulgamento")),
        "publicacao": _txt(pega("dataPublicacao", "publicacao")).strip(),
        "trecho_literal": _txt(pega("ementa")).strip(),
        "tese": _txt(pega("teseJuridica", "tese")).strip() or None,
        "tema": _txt(pega("tema")).strip() or None,
        "fonte": fonte, "origem": "dados_abertos_stj", "status": "PENDENTE",
        "aderencia": "", "_conjunto": conjunto,
    }


def buscar(argv):
    cache = _cache(argv)
    conjunto = comum.arg(argv, "--conjunto")
    classe = (comum.arg(argv, "--classe") or "").lower()
    maximo = int(comum.arg(argv, "--max", 15))
    termos = [comum.sem_acento(t.lower()) for t in re.findall(r"[\wÀ-ÿ.-]{3,}", " ".join(argv))]
    if not termos:
        sys.exit("Informe os termos da busca.")
    achados = []
    for it, fonte, conj in _registros(cache, conjunto):
        alvo = comum.sem_acento(" ".join(_txt(it.get(c)) for c in CAMPOS_TEXTO).lower())
        if not alvo or not all(t in alvo for t in termos):
            continue
        e = _entrada(it, fonte, conj)
        if classe and classe not in e["chave"].lower():
            continue
        achados.append(e)
    achados.sort(key=lambda e: e.get("julgamento") or "", reverse=True)
    for e in achados[:maximo]:
        e["trecho_literal"] = e["trecho_literal"][:1500]
    print(json.dumps({"total": len(achados), "mostrados": min(len(achados), maximo), "itens": achados[:maximo],
                      "uso": "confira a aderência ao caso; para gravar, ponha status VERIFIED, preencha "
                             "aderencia e rode ledger.py add"}, ensure_ascii=False, indent=1))
    return 0 if achados else 1


def tema(argv):
    numero = re.sub(r"\D", "", argv.pop(0)) if argv else ""
    if not numero:
        sys.exit("Uso: stj_dados_abertos.py tema <número>")
    cache = _cache(argv)
    no_campo = re.compile(rf"(?<!\d){numero}(?!\d)")
    no_texto = re.compile(rf"\btemas?\s*(?:repetitivos?\s*)?(?:n\.?\s?[º°]?\s*)?{numero}(?!\d)", re.I)
    achados = []
    for it, fonte, conj in _registros(cache):
        campo = _txt(it.get("tema")).replace(".", "")
        texto = (_txt(it.get("ementa")) + " " + _txt(it.get("notas"))).replace(".", "")
        if no_campo.search(campo) or no_texto.search(texto):
            achados.append(_entrada(it, fonte, conj))
    achados.sort(key=lambda e: e.get("julgamento") or "")
    print(json.dumps({"tema": numero, "total": len(achados), "itens": achados[:10]}, ensure_ascii=False, indent=1))
    return 0 if achados else 1


COMANDOS = {"conjuntos": conjuntos, "baixar": baixar, "buscar": buscar, "tema": tema}


def main(argv):
    comum.utf8_console()
    if not argv or argv[0] not in COMANDOS:
        print(__doc__)
        return 2
    try:
        return COMANDOS[argv[0]](argv[1:]) or 0
    except RuntimeError as e:
        print(json.dumps({"erro": str(e), "como_seguir": "rota indisponível nesta rede: siga para a página oficial "
                          "(WebFetch) ou o navegador do usuário (referencias/pesquisa_fontes.md)"},
                         ensure_ascii=False, indent=1))
        return 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
