"""Cria uma pasta que imita o acervo do Helestron, com PDFs sintéticos, capa, sigiloso e transcrições."""
import json, sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

base = Path(sys.argv[1]); base.mkdir(parents=True, exist_ok=True)
sys.dont_write_bytecode = True  # nada se grava na pasta da skill
sys.path.insert(0, sys.argv[2])
import comum

def numero(seq, ano, foro="0001"):
    return f"{seq}-{comum.digito_cnj(seq, ano, '8', '02', foro)}.{ano}.8.02.{foro}"

def pdf(caminho, paginas, marcadores):
    c = canvas.Canvas(str(caminho), pagesize=A4)
    for i, txt in enumerate(paginas):
        c.setFont("Helvetica", 9)
        c.drawString(500, 810, f"fls. {i+1}")
        y = 780
        for linha in txt.split("\n"):
            c.drawString(60, y, linha); y -= 14
        if i in marcadores:
            c.bookmarkPage(f"p{i}"); c.addOutlineEntry(marcadores[i], f"p{i}", level=0)
        c.showPage()
    c.save()

n1 = numero("0714346", "2024"); n2 = numero("0750345", "2023"); n3 = numero("0800001", "2025"); n4 = numero("0700099","2024")
pdf(base / f"{n1}.pdf", ["PETICAO INICIAL\nAcao Ordinaria. Autor militar requer promocao por ressarcimento de preterição.\nPedidos: i) promocao a Capitao; ii) efeitos financeiros.",
                         "Procuracao e documentos", "", "CONTESTACAO do Estado de Alagoas\nPreliminar de coisa julgada. Impugnacao a gratuidade.",
                         "REPLICA\nO autor reitera.", "TERMO DE AUDIENCIA\nRealizada audiencia de instrucao."],
    {0: "Petição Inicial (fls. 1-2) - 10/01/2024", 3: "Contestação (fl. 4) - 05/03/2024", 4: "Réplica (fl. 5) - 01/04/2024", 5: "Termo de Audiência (fl. 6) - 10/05/2024"})
pdf(base / f"{n2}.pdf", ["MANDADO DE SEGURANCA com pedido de liminar\nImpetrante: Tob Distribuicao Ltda", "Termo de Averiguacao n. 535280"], {0: "Petição Inicial (fls. 1-2) - 02/02/2023"})
(base / "_controle").mkdir(exist_ok=True)
json.dump({"formato": "helestron.capa/2", "sigiloso": False, "segredo": False, "prioridade": True,
           "capa": {"classe": "Procedimento Comum Cível", "assunto": "Promoção"}, "partes": [{"tipo": "Autor", "nome": "ZEDIO"}],
           "movimentacoes": [{"data": "10/09/2026", "descricao": "Conclusos para sentença"}], "audiencias": [{"data": "10/05/2024"}]},
          open(base / "_controle" / f"{n1}_capa.json", "w", encoding="utf-8"), ensure_ascii=False)
sig = base / "sigilosos" / "Lote 2026-10-08 10h00"; sig.mkdir(parents=True, exist_ok=True)
pdf(sig / f"{n3}.pdf", ["SEGREDO DE JUSTICA - dados sensiveis"], {})
(base / "notas sem numero.pdf").write_bytes((base / f"{n2}.pdf").read_bytes())
tr = base.parent / "Transcrições"; tr.mkdir(exist_ok=True)
(tr / f"Audiencia_{n1}_2024-05-10.srt").write_text("1\n00:00:01,000 --> 00:00:04,000\nJuiz: Aberta a audiência.\n\n2\n00:12:30,500 --> 00:12:35,000\nTestemunha: O autor nunca fez o curso.\n", encoding="utf-8")
json.dump({"processo": n4, "segmentos": [{"inicio": 5.2, "falante": "Juiz", "texto": "Inicio."}, {"inicio": 75, "falante": "Autor", "texto": "Fui preterido."}]},
          open(tr / "transcricao_x.json", "w", encoding="utf-8"), ensure_ascii=False)
print(json.dumps({"n1": n1, "n2": n2, "n3": n3, "n4": n4}))
