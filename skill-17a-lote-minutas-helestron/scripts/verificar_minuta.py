#!/usr/bin/env python3
"""Portão léxico e estrutural da minuta (padrão dos modelos da 17ª Vara Cível da Capital).

Uso:  python -I verificar_minuta.py <minuta.txt>
Saída: JSON com `resultado` (OK ou BLOQUEADO), `pendencias_bloqueantes` (impedem gerar o .docx) e
`apontamentos` (reexaminar um a um: só fica o que se enquadrar na exceção, com justificativa na lista
de trabalho). O verificador é rede de segurança: não substitui a leitura crítica nem a revisão
adversarial.
"""
import json
import re
import sys
sys.dont_write_bytecode = True
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import comum  # noqa: E402
import marcacao  # noqa: E402

VEDADOS = {
    r"(?i)\bcompulsando\b": "Compulsando os autos (suprimir; afirmar o resultado com as fls.)",
    r"(?i)\bin casu\b": "in casu (usar na espécie)",
    r"(?i)\bin verbis\b": "in verbis (usar só *verbis*, em itálico)",
    r"(?i)\bato cont[ií]nuo\b": "ato contínuo (usar após)",
    r"(?i)\bpois bem\b": "pois bem (suprimir)",
    r"(?i)\bante o exposto\b": "Ante o exposto (usar Diante do exposto ou Do exposto)",
    r"(?i)\bnego\b": "nego (usar indefiro)",
    r"(?i)\bno que pertine\b": "no que pertine (usar no pertinente)",
    r"(?i)\bpresentes? embargos\b": "presentes embargos (suprimir presentes)",
    r"(?i)\bem seus termos\b": "em seus termos (desnecessário)",
    r"(?i)\bhostilizad[ao]\b": "hostilizada (desnecessário)",
    r"(?i)\bem face d[ao] (senten[cç]a|decis[aã]o|ac[oó]rd[aã]o)\b": "em face da sentença (usar contra a sentença)",
    r"(?i)\bsendo assim\b": "sendo assim (usar Desse modo, Assim, Portanto, Por isso)",
    r"(?i)\bhaja vista\b": "haja vista (usar porquanto)",
    r"(?i)brevemente relatado|passo a decidir": "fórmula de outra unidade (o relatório fecha em É o Relatório.)",
    r"(?i)publica[cç][oõ]es e intima[cç][oõ]es via DJEN": "linha do DJEN não se usa na 17ª Vara",
    r"(?i)\bregistre-se\b|\bpublique-se\b": "publique-se/registre-se por extenso (o fecho da sentença é P. R. I.)",
    r"(?i)\bà fls\.": "crase indevida em 'à fls.' (usar 'à fl.' ou 'às fls.')",
    r"(?i)conclus[ãa]o inexor[áa]vel que se chega": "regência: 'a que se chega'",
    r"(?i)\bpromoa[cç][aã]o\b": "erro de digitação: promoção",
}
METODO = (r"(?i)varredura|camada de texto|\bOCR\b|renderiz|p[aá]gina a p[aá]gina|examinad[oa] visualmente|"
          r"percorrid[ao]s? (?:todas|os autos)|leitura integral|linha a linha|confrontad[oa] o CPOPG|helestron|"
          r"intelig[eê]ncia artificial|transcri[cç][aã]o autom[aá]tica|extra[cç][aã]o de texto")
PRIMEIRA_PESSOA = (r"(?i)\b(afasto|rejeito|acolho|reconhe[cç]o|entendo|verifico|observo|vislumbro|indefiro|defiro|"
                   r"julgo|condeno|determino|decido|declaro|homologo|extingo|concedo|denego|mantenho|revogo|nomeio|"
                   r"passo a|passo ao)\b")
GERUNDIO_EXC = r"^(quando|comando|comandos|mando|bando|brando|dividendo|dividendos|findo|lindo|Fernando|Orlando|Armando|Rolando|Rosendo|Raimundo|mundo|fundo|fundos|segundo|segunda|oriundo|oriunda|profundo|tremendo|estupendo|horrendo|reverendo|adendo|adendos|remendo|vendo|fazendo-se)$"
SIGLA_PALAVRA = ("DETRAN|SEFAZ|ANVISA|ANEEL|ANATEL|RENAVAM|SECOM|SENATRAN|PETROBRAS|EMBRAPA|UNESCO|DATAPREV|SEDUC|"
                 "SEPLAG|NATJUS|FUNAI|IBAMA|SERPRO|PROCON|FUNDEB|ENEM|FIES|SELIC|INCRA|DATASUS|SISBAJUD|RENAJUD|"
                 "INFOJUD|SERASAJUD|CONITEC|SESAU|SEMARH|SEINFRA|ALEPREV")
SIGLAS = ("CPC|CF|CTN|CC|STJ|STF|TJAL|TJ|SAJ|SPU|ICMS|IPVA|ITCMD|IPCA|IPCA-E|INPC|PGE|MP|OAB|CNPJ|CPF|RPV|EC|ADI|ADC|"
          "ADPF|IRDR|IAC|SUS|CDC|LEF|RJU|CNJ|CGJ|INSS|FGTS|IRPF|IPTU|ISS|AL|RJ|SP|DF|DOU|DJE|DJe|DJEN|REsp|AgInt|"
          "AREsp|RE|ARE|ED|AI|MS|RMS|ME|LTDA|EIRELI|EPP|SV|ADCT|RGPS|PM|PMAL|CBMAL|CFO|CAS|CAO|TAF|ICMS-ST|DIFAL|"
          "TUST|TUSD|UPA|CRM|CID|II|III|IV|VI|VII|VIII|IX|XI|XII|XIII|XIV|XV|XX|MANDADO|OFÍCIO|BOM")
SIGLA_MINUSC = r"\b(Pf|Bc|Onu|Oab|Inss|Bndes|Cpf|Cnpj|Stj|Stf|Cpc|Icms|Fgts|Tjal|Irdr|Rpv)\b"
STOP = ("que|para|como|pelo|pela|pelos|pelas|este|esta|esse|essa|esses|essas|nesta|neste|nessa|nesse|desta|deste|"
        "dessa|desse|quando|porque|porquanto|entretanto|todavia|contudo|portanto|inclusive|conforme|segundo|sobre|"
        "contra|entre|ainda|assim|autos|processo|parte|partes|promoção|militar|estado|alagoas")
FORMULAS_CURTAS = r"^(É o [Rr]elatório\.|P\. ?R\. ?I\.|Cumpra-se\.|Sem custas\.|Intime-se\.|Intimem-se\.)$"
LIMITE_PALAVRAS = {"sentença": 2200, "decisão": 1300, "despacho": 450}


def _palavras(t):
    return len(re.findall(r"[\wÀ-ÿ]+", t))


def _frases(t):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú])", t) if f.strip()]


def _shingles(frase, n=5):
    w = re.findall(r"[a-zà-ÿ]{3,}", comum.sem_acento(frase.lower()))
    return {" ".join(w[i:i + n]) for i in range(max(0, len(w) - n + 1))}


def verificar(caminho) -> dict:
    m = marcacao.ler(caminho)
    cfg = comum.config()["redacao"]
    pend, avis = [], []
    ato = m["ato"]
    if ato not in ("sentença", "decisão", "despacho"):
        pend.append("diretiva '@ato sentença|decisão|despacho' ausente ou inválida na primeira linha")
    if not m["processo"] or not comum.numero_cnj(m["processo"]):
        pend.append("diretiva '@processo <número CNJ>' ausente ou inválida (dá nome ao .docx; sem ela, as minutas se sobrescrevem)")
    pars = m["pars"]
    texto_pars = [p for p in pars if p["k"] not in ("nota",)]
    proprios = [p for p in texto_pars if p["k"] != "cit"]
    if not proprios:
        return {"arquivo": str(caminho), "ato": ato, "resultado": "BLOQUEADO",
                "pendencias_bloqueantes": pend + ["minuta vazia"], "apontamentos": []}

    i_rel = next((i for i, p in enumerate(texto_pars) if p["k"] == "relatorio"), -1)
    i_disp = next((i for i, p in enumerate(texto_pars) if p["k"] == "dispositivo"), -1)

    def regiao(i):
        if ato == "despacho":  # o despacho é todo ele ato decisório: 1ª pessoa admitida
            return "dispositivo"
        if i_rel >= 0 and i < i_rel:
            return "relatorio"
        if i_disp >= 0 and i >= i_disp:
            return "dispositivo"
        return "fundamentacao"

    # ---------------- estrutura do ato
    ult = marcacao.sem_marcas(proprios[-1]["txt"])
    primeiro = proprios[0]
    if ato == "sentença":
        if not re.match(r"^P\. ?R\. ?I\.$", ult):
            pend.append(f"a sentença termina em '{cfg['fecho_sentenca']}' (achado: '{ult[:40]}')")
        if i_rel < 0:
            pend.append(f"sentença sem o parágrafo '{cfg['fecho_relatorio']}'")
        if i_disp < 0:
            pend.append("sentença sem dispositivo iniciado por 'Diante do exposto, julgo …'")
        elif not re.match(r"Diante do exposto, (julgo|homologo|concedo|denego|declaro|extingo|reconheço|acolho|rejeito)\b",
                          marcacao.sem_marcas(texto_pars[i_disp]["txt"])):
            pend.append("o dispositivo da sentença abre por 'Diante do exposto, julgo' (ou homologo, concedo, denego, "
                        "declaro, extingo, reconheço, acolho, rejeito)")
        if len(proprios) >= 2:
            pen = proprios[-2]["txt"]
            if "**arquivem-se os autos com a devida baixa**" not in pen or \
                    not re.search(r"independentemente de nova determina[cç][aã]o", pen):
                pend.append("penúltimo parágrafo da sentença: " + cfg["arquivamento_sentenca"])
        depois = " ".join(marcacao.sem_marcas(p["txt"]) for i, p in enumerate(texto_pars) if i_disp >= 0 and i > i_disp)
        if i_disp >= 0 and not re.search(r"(?i)honor[aá]rios", depois):
            avis.append("sentença sem honorários após o dispositivo (no MS, consignar o art. 25 da Lei n.º 12.016/2009)")
        corpo_todo = " ".join(marcacao.sem_marcas(p["txt"]) for p in proprios)
        if re.search(r"(?i)julgo (parcialmente )?procedente", corpo_todo) and re.search(r"Estado de Alagoas|Alagoas Previd", corpo_todo) \
                and not re.search(r"(?i)remessa necess[aá]ria|reexame necess[aá]rio|art\. 496", corpo_todo):
            avis.append("procedência contra a Fazenda sem consignar a sujeição (ou não) à remessa necessária (art. 496 do CPC)")
    elif ato in ("decisão", "despacho"):
        if ult != cfg["fecho_decisao"]:
            pend.append(f"a {ato} termina em '{cfg['fecho_decisao']}' (achado: '{ult[:40]}')")
        if ato == "decisão" and i_disp < 0:
            avis.append("decisão sem parágrafo iniciado por 'Diante do exposto' ou 'Do exposto'")
    if ato in ("sentença", "decisão") and i_rel >= 0:
        p1 = primeiro["txt"]
        if not marcacao.sem_marcas(p1).startswith("Trata-se de "):
            pend.append("o relatório abre por 'Trata-se de …' (classe, partes em negrito)")
        elif "**" not in p1:
            pend.append("1º parágrafo sem os nomes das partes em negrito (**Nome Completo**)")
        if re.match(r"(?i)^Trata-se de a[cç][aã]o (de|declarat|indeniz|cobran|anulat|condenat)", marcacao.sem_marcas(p1)):
            avis.append("classe no 1º parágrafo: 'Ação Ordinária' para as ações de conhecimento (salvo MS, ACP, "
                        "Ação Popular e Desapropriação)")

    # ---------------- varredura parágrafo a parágrafo
    total_palavras, palavras_cit, serie_cit, vistos = 0, 0, 0, []
    for i, p in enumerate(texto_pars):
        k, bruto = p["k"], p["txt"]
        t = marcacao.sem_marcas(bruto)
        ref = f"linha {p['linha']}"
        reg = regiao(i)
        w = _palavras(t)
        total_palavras += w
        for e in marcacao.desbalanceado(bruto):
            pend.append(f"marcação {e} na {ref}")
        if k == "cit":
            palavras_cit += w
            julgado = re.search(r"Rel(?:\.|ator|atora)\b|julgad[oa] (?:em|monocraticamente)|\bDJe?\b|\bj\.\s*\d|"
                                r"\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}", t)
            serie_cit = serie_cit + 1 if julgado else 0
            if serie_cit == 3:
                avis.append(f"precedentes em série ({ref}): baste o mais pertinente, com a tese que decide")
            continue
        serie_cit = 0
        sem_aspas = re.sub(r'"[^"]*"|“[^”]*”', "", t)
        if re.match(r"^\(?\d{1,3}[.)]\s+\S|^\d{1,3}\.\t|^[IVX]{1,5}\s*[-–—.)]\s", t) and k != "cit":
            pend.append(f"numeração manual de parágrafo na {ref} (a numeração é aplicada no SAJ)")
        if k == "corpo" and re.fullmatch(r"\*\*[^*]+\*\*\.?", bruto.strip()):
            pend.append(f"parágrafo inteiro em negrito na {ref} (epígrafe disfarçada; conclusão decisória vai com '!! ')")
        if k in ("corpo", "decisorio") and w <= 8 and not re.match(FORMULAS_CURTAS, t) and \
                (re.match(r"^(D[aoe]s?|DA|DO|DOS|DAS)\s", t) or not re.search(r"[.!?:;]$", t) or t.isupper()):
            pend.append(f"possível título ou epígrafe interna na {ref}: '{t}'")
        for rx, msg in VEDADOS.items():
            if re.search(rx, sem_aspas):
                pend.append(f"{msg} — {ref}")
        if re.search(METODO, sem_aspas):
            pend.append(f"linguagem de método na {ref} (afirme o resultado, com as fls.)")
        if reg != "dispositivo" and k not in ("decisorio", "comando", "sublinhado"):
            for f in re.finditer(PRIMEIRA_PESSOA, sem_aspas):
                pend.append(f"1ª pessoa fora do dispositivo na {ref}: '{f.group(0)}' (forma impessoal, ou "
                            f"parágrafo decisório '!! ' na conclusão de preliminar)")
        if re.search(r"À SPU\s*:", t):
            pend.append(f"'À SPU' seguido de dois-pontos na {ref}")
        for q in re.finditer(r'"([^"]+)"|“([^”]+)”', t):
            if _palavras(q.group(0)) > 55:
                pend.append(f"citação de {_palavras(q.group(0))} palavras entre aspas na {ref}: vai em bloco ('> ')")
        for x in re.finditer(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{4,}\b", t):
            if re.fullmatch(SIGLA_PALAVRA, x.group(0)):
                pend.append(f"sigla pronunciada como palavra na {ref}: '{x.group(0)}' (só a inicial maiúscula)")
            elif not re.fullmatch(SIGLAS, x.group(0)):
                avis.append(f"caixa alta possivelmente indevida na {ref}: '{x.group(0)}'")
        if re.search(r"(?i)\b(defiro|determino|deferida|determinada)\b.{0,80}\b(prova pericial|per[íi]cia)\b", t) and \
                not re.search(r"(?i)nomeio|nomeado|nomeada", " ".join(marcacao.sem_marcas(x["txt"]) for x in texto_pars)):
            pend.append(f"perícia deferida sem perito nomeado na própria minuta ({ref})")
        if "{{!" in bruto and not re.search(r"(?i)sisbajud|renajud|bloqueio|restri[cç][aã]o", t + bruto):
            avis.append(f"vermelho que fica na limpa ({{{{! }}}}) fora de Sisbajud/Renajud na {ref}")
        if k == "dispositivo" and "**" in bruto:
            avis.append(f"'**' no dispositivo ({ref}): o gerador já põe o parágrafo inteiro em negrito e sublinhado")
        # apontamentos de estilo
        for g in re.finditer(r"\b[A-Za-zÀ-ÿ][a-zà-ÿ]*(ando|endo|indo|ondo)\b", sem_aspas.replace("tendo em vista", "")):
            if not re.match(GERUNDIO_EXC, g.group(0), re.I):
                avis.append(f"gerúndio na {ref}: '{g.group(0)}' (forma nominal ou oração desenvolvida)")
        if " — " in t or " – " in t:
            avis.append(f"travessão na {ref} (só quando essencial)")
        prox = texto_pars[i + 1]["k"] if i + 1 < len(texto_pars) else None
        if ":" in re.sub(r"https?:", "", sem_aspas) and not (t.endswith(":") and prox == "cit"):
            avis.append(f"dois-pontos no corpo na {ref} (só para introduzir transcrição em bloco)")
        if w > cfg["max_palavras_paragrafo_bloqueante"]:
            pend.append(f"parágrafo de {w} palavras na {ref} (divida: uma questão por parágrafo)")
        elif w > cfg["max_palavras_paragrafo"]:
            avis.append(f"parágrafo de {w} palavras na {ref} (padrão: até 5 ou 6 linhas)")
        if reg == "fundamentacao" and k == "corpo" and w <= 6 and not re.match(FORMULAS_CURTAS, t):
            avis.append(f"frase curta e solta na fundamentação ({ref}): '{t}'")
        if w <= 14 and re.match(r"^(Não|Nada|Nenhum|Nenhuma|Inexiste|Sem razão)\b", t) and reg == "fundamentacao":
            avis.append(f"parágrafo abre negando o direito em frase curta ({ref}): conduza o leitor até a conclusão")
        if reg == "relatorio" and re.search(r"\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{1,2}h\d{2}\b", t):
            avis.append(f"data ou horário no relatório ({ref}): só se a data for o próprio fato a decidir")
        if re.search(r"(?i)\btema\s+(n\.º\s*)?\d|repetitiv|repercuss[aã]o geral", t):
            avis.append(f"menção a tema na {ref}: só se aplicado ao caso ou invocado pela parte")
        if re.search(r"(?i)certifique-se|certifique a secretaria|conte-se o prazo", t):
            avis.append(f"comando de certificação ou contagem na {ref} (só evento fora dos autos)")
        if re.search(r"(?i)\bposto que\b", t):
            avis.append(f"'posto que' na {ref}: é concessiva; para causa, use 'porquanto' ou 'uma vez que'")
        if re.search(r"§\d", t):
            avis.append(f"grafia na {ref}: '§ 8º' (com espaço)")
        if re.search(r"\bn[º°]\s*\d|\bN[º°]\s*\d|\bn\.\s?\d", t):
            avis.append(f"grafia na {ref}: 'n.º' para o número")
        for x in re.finditer(SIGLA_MINUSC, t):
            avis.append(f"sigla em minúsculas na {ref}: '{x.group(0)}'")
        cont = {}
        for x in re.findall(r"\b[A-Za-zÀ-ÿ]{7,}\b", sem_aspas):
            k2 = x.lower()
            if not re.fullmatch(STOP, k2):
                cont[k2] = cont.get(k2, 0) + 1
        for k2, c in cont.items():
            if c >= 4:
                avis.append(f"palavra repetida {c} vezes na {ref}: '{k2}'")
        if reg != "relatorio":
            for f in _frases(t):
                sh = _shingles(f)
                if len(sh) < 4:
                    continue
                for anterior, ref_ant in vistos:
                    if len(sh & anterior) / len(sh) > 0.6:
                        avis.append(f"ideia repetida na {ref} (já dita na {ref_ant}): enxugue")
                        break
                vistos.append((sh, ref))

    # ---------------- extensão (contra a verborragia)
    limite = LIMITE_PALAVRAS.get(ato)
    if limite and total_palavras > limite:
        avis.append(f"{ato} com {total_palavras} palavras (referência: até {limite}); suprima o que não decide")
    if ato == "sentença" and total_palavras and palavras_cit / total_palavras > 0.40:
        avis.append(f"transcrições somam {round(100 * palavras_cit / total_palavras)}% do texto: transcreva só o que decide")
    return {"arquivo": str(caminho), "ato": ato, "paragrafos": len(texto_pars), "palavras": total_palavras,
            "resultado": "BLOQUEADO" if pend else "OK", "pendencias_bloqueantes": pend,
            "apontamentos": list(dict.fromkeys(avis))}


def main(argv):
    comum.utf8_console()
    if not argv:
        print(__doc__)
        return 2
    r = verificar(Path(argv[0]))
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r["resultado"] == "OK" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
