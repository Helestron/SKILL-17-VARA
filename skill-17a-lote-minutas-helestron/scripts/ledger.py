#!/usr/bin/env python3
"""Ledger de verificações (precedentes, súmulas, temas, normas, doutrina) e de cálculos.

A minuta só cita o que tem entrada VERIFIED aqui, e só afirma valor que o ledger de cálculos
registra. Uma entrada por arquivo em `<trabalho>/verificacoes/<ID>.json` (subagentes em paralelo
não disputam o mesmo arquivo). Entrada VERIFIED conferida há menos de 30 dias é reaproveitada nos
lotes seguintes (cache), sem nova pesquisa.

Verificações (todos com --trabalho <dir>):
  add ARQ.json|-            grava uma entrada ou uma lista; valida campos e fonte; imprime os IDs
  get ID | listar [--tipo T] | buscar TERMO… [--todos]
  conferir MINUTA.txt [--calculos calculos.json]
        confronta as citações do texto próprio da minuta com o ledger: precedente, súmula ou tema
        sem entrada VERIFIED é pendência bloqueante; valor em R$ sem lastro no ledger de cálculos
        é apontamento
Cálculos (arquivo do processo, `autos.py caminhos N` → "calculos"):
  calc ARQ add --descricao TXT --expr "EXPRESSÃO" [--fls F] [--casas 2]
        (números no formato brasileiro, "4.908,00", ou com ponto; argumentos separados por vírgula
        e espaço: "round(4908 / 1412, 2)")
        avalia a expressão (só números e + - * / ** ( ), round, min, max) e registra entrada,
        operação, resultado e data — nenhuma conta entra na minuta "de cabeça"
  calc ARQ entrada --descricao TXT --valor V --fls F      registra valor colhido dos autos
  calc ARQ listar

Esquema da verificação (VERIFIED exige os campos do tipo):
  comuns:      id (gerado), tipo, chave (como a minuta cita), fonte (URL), status, conferido_em
  precedente:  tribunal, orgao, relator, julgamento (AAAA-MM-DD), publicacao, trecho_literal (ementa
               ou trecho), aderencia (por que serve ao caso)
  sumula/tema: tribunal, trecho_literal (enunciado ou tese, literal), aderencia
  dispositivo: trecho_literal (redação vigente), fonte no Planalto ou no SAPL
  doutrina:    autor, obra, edicao, editora, ano, pagina, trecho_literal (conferidos na fonte)
  ato_normativo: trecho_literal
Fonte: lei no Planalto/SAPL; jurisprudência no STF, no STJ (inclusive dados abertos) ou no TJAL;
o JusBrasil vale só para comprovar a autenticidade do inteiro teor ou da ementa oficial (anote
`origem: "jusbrasil"`). Assistente generativo (JusIA e afins) nunca é fonte.
"""
import ast
import json
import operator
import re
import sys
sys.dont_write_bytecode = True
import unicodedata
from datetime import date, datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402
import marcacao  # noqa: E402

TIPOS = {"precedente", "sumula", "tema", "dispositivo", "doutrina", "ato_normativo"}
STATUS = {"VERIFIED", "REJECTED", "PENDENTE"}
OBRIGATORIOS = {
    "precedente": ["tribunal", "orgao", "relator", "julgamento", "trecho_literal", "aderencia"],
    "sumula": ["tribunal", "trecho_literal", "aderencia"],
    "tema": ["tribunal", "trecho_literal", "aderencia"],
    "dispositivo": ["trecho_literal"],
    "doutrina": ["autor", "obra", "editora", "ano", "pagina", "trecho_literal"],
    "ato_normativo": ["trecho_literal"],
}
VALIDADE_DIAS = 30

NUM = r"(?:n\.?\s?[º°o]?\.?\s*)?(\d(?:[\d.]{0,11}\d)?)"
CLASSES_STJ = r"REsp|AREsp|AgInt(?:\s+no|\s+nos)?\s+(?:REsp|AREsp)|AgRg(?:\s+no|\s+nos)?\s+(?:REsp|AREsp)|EREsp|EDcl(?:\s+no|\s+nos)?\s+(?:REsp|AREsp)|RMS|CC"
CLASSES_STF = r"RE|ARE|ADI|ADC|ADPF|ADO|Rcl|AI(?:-AgR)?|RMS"
PREC_RE = re.compile(rf"\b((?:{CLASSES_STJ})|(?:{CLASSES_STF})|MS|HC|IRDR|IAC)\s+{NUM}", re.I)
SUM_RE = re.compile(r"\bS[úu]mula\s+(Vinculante\s+)?(?:n\.?\s?[º°]?\s*)?(\d{1,4})(?:(?:\s*/\s*|\s+d[oa]\s+)(STJ|STF|TJAL))?", re.I)
SV_RE = re.compile(r"\bSV\s+(\d{1,3})\b")
TEMA_RE = re.compile(r"\bTema\s+(?:n\.?\s?[º°]?\s*)?(\d(?:[\d.]{0,5}\d)?)(?:(?:\s*/\s*|\s+d[oa]\s+)(STJ|STF|TJAL))?", re.I)
CNJ_PREC_RE = re.compile(r"\b(Apela[çc][ãa]o C[íi]vel|Agravo de Instrumento|Agravo Interno|Embargos de Declara[çc][ãa]o|"
                         r"Remessa Necess[áa]ria|A[çc][ãa]o Rescis[óo]ria|Mandado de Seguran[çc]a).{0,40}?"
                         r"(\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4})", re.I)
DINHEIRO_RE = re.compile(r"R\$\s?(\d{1,3}(?:\.\d{3})*,\d{2})")


def _seguro(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9-]+", "-", s).strip("-").upper()[:80]


def _digitos(s):
    return re.sub(r"\D", "", s or "")


def chaves(texto: str) -> list:
    """Citações normalizadas do texto: [(chave_norm, trecho)]."""
    out = []
    for m in PREC_RE.finditer(texto):
        classe = re.sub(r"\s+", " ", m.group(1)).upper()
        base = classe.split()[-1]  # AgInt no REsp → REsp (o número é o do recurso)
        out.append((f"PREC:{base}:{_digitos(m.group(2))}", m.group(0)))
    for m in SUM_RE.finditer(texto):
        trib = "STF" if m.group(1) else (m.group(3) or "?").upper()
        out.append((f"SUM:{'SV' if m.group(1) else trib}:{_digitos(m.group(2))}", m.group(0)))
    for m in SV_RE.finditer(texto):
        out.append((f"SUM:SV:{m.group(1)}", m.group(0)))
    for m in TEMA_RE.finditer(texto):
        out.append((f"TEMA:{(m.group(2) or '?').upper()}:{_digitos(m.group(1))}", m.group(0)))
    for m in CNJ_PREC_RE.finditer(texto):
        out.append((f"PREC:CNJ:{_digitos(m.group(2))}", m.group(0)))
    vistos, unicos = set(), []
    for k, t in out:
        if k not in vistos:
            vistos.add(k)
            unicos.append((k, t))
    return unicos


def _casa(k_minuta: str, k_ledger: str) -> bool:
    a, b = k_minuta.split(":"), k_ledger.split(":")
    if a[0] != b[0] or a[-1] != b[-1]:
        return False
    return a[1] == b[1] or "?" in (a[1], b[1]) or a[0] == "PREC"


# ---------------------------------------------------------------- verificações

def pasta(trab: Path) -> Path:
    p = trab / "verificacoes"
    p.mkdir(parents=True, exist_ok=True)
    return p


def todas(trab: Path) -> list:
    saida = []
    for f in sorted(pasta(trab).glob("*.json")):
        try:
            saida.append(json.loads(f.read_text(encoding="utf-8-sig")))
        except (OSError, ValueError):
            pass
    return saida


def valida(e: dict) -> list:
    erros = []
    if e.get("tipo") not in TIPOS:
        erros.append(f"tipo inválido: {e.get('tipo')}")
    if e.get("status") not in STATUS:
        erros.append(f"status inválido: {e.get('status')}")
    if not e.get("chave"):
        erros.append("chave ausente (como a minuta cita)")
    if e.get("status") == "VERIFIED":
        for c in OBRIGATORIOS.get(e.get("tipo"), []):
            if not str(e.get(c) or "").strip():
                erros.append(f"campo obrigatório ausente: {c}")
        if e.get("tipo") != "doutrina":
            tipo_fonte = "lei" if e.get("tipo") == "dispositivo" else e.get("tipo")
            if not comum.dominio_oficial(e.get("fonte", ""), tipo_fonte):
                erros.append(f"fonte não oficial para {e.get('tipo')}: {e.get('fonte')}")
        if len(str(e.get("trecho_literal") or "")) < 20:
            erros.append("trecho_literal curto demais: transcreva o texto conferido")
    return erros


def add(trab, argv):
    if not argv:
        sys.exit("Uso: ledger.py add <arquivo.json>|- -t <T>")
    bruto = sys.stdin.read() if argv[0] == "-" else Path(argv[0]).read_text(encoding="utf-8-sig")
    dados = json.loads(bruto)
    lista = dados if isinstance(dados, list) else [dados]
    falhou = False
    for e in lista:
        e.setdefault("conferido_em", comum.hoje())
        e["id"] = e.get("id") or _seguro(f"{e.get('tipo', 'x')}-{e.get('chave', '')}")
        e["chaves_norm"] = [k for k, _ in chaves(e.get("chave", ""))]
        erros = valida(e)
        if erros:
            falhou = True
            print(json.dumps({"id": e["id"], "gravado": False, "erros": erros}, ensure_ascii=False))
            continue
        comum.gravar_json(pasta(trab) / f"{e['id']}.json", e)
        print(json.dumps({"id": e["id"], "gravado": True, "status": e["status"]}, ensure_ascii=False))
    return 1 if falhou else 0


def valida_ainda(e) -> bool:
    try:
        dias = (date.today() - date.fromisoformat(e.get("conferido_em", "1900-01-01"))).days
    except ValueError:
        return False
    return dias <= VALIDADE_DIAS


def buscar(trab, argv):
    todos = comum.flag(argv, "--todos")
    termos = [comum.sem_acento(t.lower()) for t in argv]
    for e in todas(trab):
        alvo = comum.sem_acento(json.dumps(e, ensure_ascii=False).lower())
        if all(t in alvo for t in termos) and (todos or e.get("status") == "VERIFIED"):
            print(json.dumps({"id": e["id"], "status": e["status"], "chave": e.get("chave"),
                              "conferido_em": e.get("conferido_em"),
                              "valida": valida_ainda(e)}, ensure_ascii=False))
    return 0


def conferir(trab, argv):
    calc_arq = comum.arg(argv, "--calculos")
    m = marcacao.ler(argv[0])
    proprio = " ".join(marcacao.sem_marcas(p["txt"]) for p in m["pars"] if p["k"] not in ("cit", "nota"))
    transcrito = " ".join(marcacao.sem_marcas(p["txt"]) for p in m["pars"] if p["k"] == "cit")
    ledger = [e for e in todas(trab) if e.get("status") == "VERIFIED"]
    rejeitadas = [e for e in todas(trab) if e.get("status") == "REJECTED"]
    pend, avis, ok = [], [], []
    for k, trecho in chaves(proprio):
        achou = next((e for e in ledger if any(_casa(k, kl) for kl in e.get("chaves_norm", []))), None)
        rej = next((e for e in rejeitadas if any(_casa(k, kl) for kl in e.get("chaves_norm", []))), None)
        if rej and not achou:
            pend.append(f"'{trecho}' consta como REJECTED no ledger ({rej['id']}): retire-o da minuta")
        elif not achou:
            pend.append(f"'{trecho}' sem entrada VERIFIED no ledger: confira na fonte oficial ou retire")
        else:
            ok.append(achou["id"])
            if not valida_ainda(achou):
                avis.append(f"'{trecho}': conferência de {achou['conferido_em']} com mais de {VALIDADE_DIAS} dias; reconfira")
    for k, trecho in chaves(transcrito):
        if not any(any(_casa(k, kl) for kl in e.get("chaves_norm", [])) for e in ledger):
            avis.append(f"'{trecho}' aparece dentro de transcrição: confira se a transcrição é literal da fonte")
    if calc_arq:
        calc = comum.ler_json(calc_arq, {"itens": []})
        lastro = " ".join(json.dumps(i, ensure_ascii=False) for i in calc.get("itens", []))
        for v in DINHEIRO_RE.findall(proprio):
            if v not in lastro:
                avis.append(f"valor R$ {v} sem lastro no ledger de cálculos (registre a entrada com as fls. ou o cálculo)")
    print(json.dumps({"minuta": argv[0], "resultado": "BLOQUEADO" if pend else "OK", "conferidas": sorted(set(ok)),
                      "pendencias_bloqueantes": pend, "apontamentos": list(dict.fromkeys(avis))},
                     ensure_ascii=False, indent=1))
    return 1 if pend else 0


# ---------------------------------------------------------------- cálculos

OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
       ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos}
FUNCOES = {"round": round, "min": min, "max": max, "abs": abs}


def _avaliar(no):
    if isinstance(no, ast.Expression):
        return _avaliar(no.body)
    if isinstance(no, ast.Constant) and isinstance(no.value, (int, float)):
        return no.value
    if isinstance(no, ast.BinOp) and type(no.op) in OPS:
        return OPS[type(no.op)](_avaliar(no.left), _avaliar(no.right))
    if isinstance(no, ast.UnaryOp) and type(no.op) in OPS:
        return OPS[type(no.op)](_avaliar(no.operand))
    if isinstance(no, ast.Call) and isinstance(no.func, ast.Name) and no.func.id in FUNCOES:
        return FUNCOES[no.func.id](*[_avaliar(a) for a in no.args])
    raise ValueError("expressão não permitida (só números, + - * / ** ( ), round, min, max, abs)")


def _decimal_br(expr: str) -> str:
    """'4.908,00' → 4908.00 e '1412,5' → 1412.5; a vírgula seguida de espaço separa argumentos
    (round(x, 2), min(a, b))."""
    expr = re.sub(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?", lambda m: m.group(0).replace(".", "").replace(",", "."), expr)
    return re.sub(r"(?<=\d),(?=\d)", ".", expr)


def _brl(v: float) -> str:
    s = f"{v:,.2f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def calc(argv):
    if len(argv) < 2:
        sys.exit("Uso: ledger.py calc <calculos.json> add|entrada|listar …")
    arq, acao, resto = Path(argv[0]), argv[1], argv[2:]
    dados = comum.ler_json(arq, {"itens": []})
    if acao == "listar":
        print(json.dumps(dados, ensure_ascii=False, indent=1))
        return 0
    desc = comum.arg(resto, "--descricao")
    fls = comum.arg(resto, "--fls")
    if not desc:
        sys.exit("Informe --descricao.")
    item = {"n": len(dados["itens"]) + 1, "descricao": desc, "fls": fls,
            "registrado": datetime.now().isoformat(timespec="seconds")}
    if acao == "entrada":
        valor = comum.arg(resto, "--valor")
        item.update({"tipo": "entrada", "valor": valor})
    elif acao == "add":
        expr = comum.arg(resto, "--expr")
        casas = int(comum.arg(resto, "--casas", 2))
        try:
            resultado = round(_avaliar(ast.parse(_decimal_br(expr or ""), mode="eval")), casas)
        except (ValueError, SyntaxError, ZeroDivisionError, TypeError) as e:
            sys.exit(f"cálculo recusado: {e}")
        item.update({"tipo": "calculo", "expressao": expr, "resultado": resultado,
                     "resultado_brl": _brl(resultado)})
    else:
        sys.exit(f"Ação desconhecida: {acao}")
    dados["itens"].append(item)
    comum.gravar_json(arq, dados)
    print(json.dumps(item, ensure_ascii=False))
    return 0


def main(argv):
    comum.utf8_console()
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    if argv[0] == "calc":
        return calc(argv[1:])
    cmd, resto = argv[0], argv[1:]
    trab = comum.pasta_trabalho(resto)
    if cmd == "add":
        return add(trab, resto)
    if cmd == "get":
        e = next((x for x in todas(trab) if x["id"] == resto[0]), None)
        print(json.dumps(e, ensure_ascii=False, indent=1) if e else "não encontrado")
        return 0 if e else 1
    if cmd == "listar":
        tipo = comum.arg(resto, "--tipo")
        for e in todas(trab):
            if not tipo or e.get("tipo") == tipo:
                print(f"{e['id']} | {e.get('status')} | {e.get('chave')} | {e.get('conferido_em')}")
        return 0
    if cmd == "buscar":
        return buscar(trab, resto)
    if cmd == "conferir":
        return conferir(trab, resto)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
