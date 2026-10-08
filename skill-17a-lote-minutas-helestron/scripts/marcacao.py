#!/usr/bin/env python3
"""Marcação da minuta (referencias/formato_minuta.md) — leitura comum ao gerador e ao verificador.

Uma linha por parágrafo; linhas em branco não contam. Os parágrafos NÃO são numerados: a
numeração é aplicada pelo usuário no editor do SAJ, no lançamento manual.

Diretivas (topo do arquivo):  @ato sentença|decisão|despacho   @processo <número CNJ>
Prefixos de linha:
  (nenhum)  parágrafo do corpo
  > texto   transcrição em bloco (lei, tese, súmula, ementa, trecho longo): Courier New 10, recuo de 4 cm
  !! texto  parágrafo decisório em destaque (negrito e sublinhado inteiros): conclusão de preliminar,
            prejudicial ou incidente e a tese central do mérito, como nos modelos
  __ texto  parágrafo inteiro sublinhado (comandos de cumprimento)
  + texto   item de enumeração recuado (4 cm), v.g. "i) planilha de cálculo atualizada…"
  ++ texto  subitem recuado (4,5 cm), v.g. "a) contribuições previdenciárias…"
            (itens que seguem o dispositivo ou um comando saem sublinhados, como nos modelos)
  %% texto  nota só da versão anotada (vermelho)
  // texto  comentário (ignorado)
Automático: "É o Relatório." em negrito; o dispositivo ("Diante do exposto…", "Do exposto…") em
negrito e sublinhado; depois do dispositivo, o parágrafo que abre por verbo de comando
("Intime-se", "Expeça-se", "Após,", "Serve a presente"…) sublinhado.
Em linha: **negrito**  __sublinhado__  *itálico*  {{apontamento vermelho, só na anotada}}
          {{! dado vermelho que fica também na limpa (só Sisbajud/Renajud)}}   \\* asterisco literal
"""
import re
import sys
sys.dont_write_bytecode = True
from pathlib import Path

DISPOSITIVO_RE = re.compile(r"^(Diante do exposto|Do exposto|Pelo exposto|Por todo o exposto|Ante o exposto|"
                            r"Isto posto|Posto isso|Em face do exposto)\b")
COMANDO_RE = re.compile(r"^(À SPU|À Secretaria|Ao Cartório|Intime(?:m)?-se|Cite(?:m)?-se|Notifique(?:m)?-se|"
                        r"Expeça(?:m)?-se|Oficie(?:m)?-se|Retire-se|Retire|Cadastre-se|Cadastre|Retifique-se|"
                        r"Proceda-se|Dê-se|Remetam-se|Remeta-se|Encaminhem-se|Encaminhe-se|Junte-se|Aguarde-se|"
                        r"Após|Em seguida|Serve a presente|Certifique-se|Anote-se|Anotem-se|Inclua-se|Exclua-se|"
                        r"Libere-se|Desbloqueie-se|Requisite-se|Comunique-se|Providencie|Promova|Abra-se|Tornem|"
                        r"Voltem|Façam-se|Faça-se|Ciência|Suspenda-se|Suspendam-se|Sobreste-se|Sobrestem-se|"
                        r"Arquive-se|Arquivem-se|Designe-se|Decorrido|Decorridos|Retornem|Retorne|Aguardem|"
                        r"Cumpra(?:m)?-se o|Publique-se o edital|Citem-se|Por derradeiro|Exaurido|Exauridos|"
                        r"Com a indicação|Com a manifestação|Com o cumprimento|Com a juntada|Com a resposta|"
                        r"Mantenha-se|Mantenham-se|Determino, ainda|Não havendo|Havendo|Ultimad[oa]s?)\b")
FECHO_DECISAO_RE = re.compile(r"^Cumpra-se(,? observada a sequência acima)?\.$")
RELATORIO_RE = re.compile(r"^É o [Rr]elatório\.$")
TIPOS_ATO = {"sentenca": "sentença", "sentença": "sentença", "decisao": "decisão", "decisão": "decisão",
             "despacho": "despacho"}


def _limpar_ato(valor: str) -> str:
    v = (valor or "").strip().lower()
    return TIPOS_ATO.get(v, v)


def ler(caminho) -> dict:
    """{'ato', 'processo', 'pars': [{'k': tipo, 'txt': texto, 'linha': n}]}.
    Tipos: corpo, cit, item1, item2, decisorio, sublinhado, nota, relatorio, dispositivo, comando.
    O item traz 'ordem' verdadeiro quando segue o dispositivo, um comando ou parágrafo sublinhado."""
    linhas = Path(caminho).read_text(encoding="utf-8-sig").splitlines()
    out = {"ato": None, "processo": None, "pars": []}
    apos_disp = False
    ultimo = None  # tipo do último parágrafo que não é item de enumeração
    for i, bruta in enumerate(linhas, 1):
        ln = bruta.rstrip()
        if not ln.strip() or ln.lstrip().startswith("//"):
            continue
        if ln.startswith("@ato "):
            out["ato"] = _limpar_ato(ln[5:])
            apos_disp = out["ato"] == "despacho"  # no despacho, os comandos se sublinham desde o início
            continue
        if ln.startswith("@processo "):
            out["processo"] = ln[10:].strip()
            continue
        if ln.startswith("%%"):
            out["pars"].append({"k": "nota", "txt": ln[2:].strip(), "linha": i})
            continue
        if ln.startswith(">"):
            out["pars"].append({"k": "cit", "txt": ln[1:].strip(), "linha": i})
            continue
        if ln.startswith("++ ") or ln.startswith("+ "):
            nivel = "item2" if ln.startswith("++ ") else "item1"
            out["pars"].append({"k": nivel, "txt": ln[3 if nivel == "item2" else 2:].strip(), "linha": i,
                                "ordem": ultimo in ("dispositivo", "decisorio", "comando", "sublinhado")})
            continue
        if ln.startswith("!! "):
            k, txt = "decisorio", ln[3:].strip()
        elif ln.startswith("__ "):
            k, txt = "sublinhado", ln[3:].strip()
        else:
            k, txt = "corpo", ln.strip()
        plano = sem_marcas(txt)
        if RELATORIO_RE.match(plano):
            k = "relatorio"
        elif DISPOSITIVO_RE.match(plano):
            k, apos_disp = "dispositivo", True
        elif apos_disp and k == "corpo" and COMANDO_RE.match(plano):
            k = "comando"
        out["pars"].append({"k": k, "txt": txt, "linha": i})
        ultimo = k
    return out


def sem_marcas(txt: str, manter_vermelho=False) -> str:
    """Texto sem marcação; por padrão sem os apontamentos {{…}} (mantém o {{! …}} se pedido)."""
    s = re.sub(r"\{\{!\s*(.*?)\}\}", (lambda m: m.group(1)) if manter_vermelho else "", txt)
    s = re.sub(r"\{\{.*?\}\}", "", s)
    s = s.replace("**", "").replace("__", "")
    s = re.sub(r"(?<!\\)\*", "", s).replace("\\*", "*")
    return re.sub(r"\s{2,}", " ", s).strip()


def runs(txt: str) -> list:
    """Divide o texto em trechos com estado: [{'t', 'b', 'u', 'i', 'red', 'fica'}].
    'red' = apontamento ({{ }}), 'fica' = vermelho que permanece na limpa ({{! }})."""
    out, buf = [], []
    st = {"b": False, "u": False, "i": False, "red": False, "fica": False}

    def flush():
        if buf:
            out.append({"t": "".join(buf), **st})
            buf.clear()

    i, n = 0, len(txt)
    while i < n:
        if txt.startswith("\\*", i):
            buf.append("*")
            i += 2
            continue
        if txt.startswith("{{!", i) and not st["red"]:
            flush()
            st["red"], st["fica"] = True, True
            i += 3
            while i < n and txt[i] == " ":
                i += 1
            continue
        if txt.startswith("{{", i) and not st["red"]:
            flush()
            st["red"], st["fica"] = True, False
            i += 2
            continue
        if txt.startswith("}}", i) and st["red"]:
            flush()
            st["red"], st["fica"] = False, False
            i += 2
            continue
        if txt.startswith("**", i):
            flush()
            st["b"] = not st["b"]
            i += 2
            continue
        if txt.startswith("__", i):
            flush()
            st["u"] = not st["u"]
            i += 2
            continue
        if txt[i] == "*":
            flush()
            st["i"] = not st["i"]
            i += 1
            continue
        buf.append(txt[i])
        i += 1
    flush()
    return out


def desbalanceado(txt: str) -> list:
    """Marcas abertas e não fechadas no parágrafo (pendência bloqueante)."""
    erros = []
    s = txt.replace("\\*", "")
    if s.count("{{") != s.count("}}"):
        erros.append("{{ }} desbalanceado")
    s2 = re.sub(r"\{\{.*?\}\}", "", s)
    if s2.count("**") % 2:
        erros.append("** desbalanceado")
    if s2.count("__") % 2:
        erros.append("__ desbalanceado")
    if s2.replace("**", "").count("*") % 2:
        erros.append("* (itálico) desbalanceado")
    return erros
