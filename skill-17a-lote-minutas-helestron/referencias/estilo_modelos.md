# Padrão estilístico da 17ª Vara — o que os modelos ensinam

Os modelos da vara (`modelos/`) são o **padrão de estrutura, de perfil de análise, de retórica e de
linguagem** de toda minuta. Este arquivo destila o que eles têm em comum e diz o que conservar, o que
enxugar e o que corrigir. Leia-o antes da primeira minuta do lote; antes de cada minuta, abra o
modelo de tema mais próximo (`importar_modelo.py buscar "<classe> <tema> <desfecho>"`).

O modelo é **diretriz, não teto nem molde para colar**: segue-se a arquitetura e a voz do juízo, com
a redação mais objetiva que o item 6 pede, sem reproduzir os vícios do item 9 e sem jamais citar
precedente que o modelo traga sem conferência (Fase 2 do SKILL.md).

## 1. Biblioteca

| Arquivo (em `modelos/`, marcação; original em `modelos/originais/`) | Ato | Tema | Desfecho |
|---|---|---|---|
| `sentenca_promocao_militar_ativo_com_saltos_IRDR_coisa_julgada_improcedencia.txt` | sentença | promoção por ressarcimento de preterição, ativo, *per saltum*, IRDR n.º 3/TJAL, coisa julgada e gratuidade | improcedência |
| `sentenca_promocao_militar_ativo_sem_saltos_improcedencia.txt` | sentença | promoção, ativo, sem saltos, exclusão de ofício da Alagoas Previdência, curso feito *a posteriori*, fato superveniente | improcedência |
| `sentenca_promocao_militar_inativo_correcao_anteriores_coisa_julgada_improcedencia.txt` | sentença | promoção, inativo, correção de promoções anteriores, prescrição por ato comissivo e omissivo | improcedência |
| `decisao_MS_tributario_liberacao_mercadorias_ICMS_liminar_defere_em_parte.txt` | decisão | MS tributário, apreensão de mercadorias como coerção (Súmula 323/STF), pedido preventivo genérico | liminar deferida em parte |

Novos modelos entram por `importar_modelo.py <arquivo> --saida modelos/<nome>.txt` (proposta ao
usuário no fim do lote, seção "Autodesenvolvimento" do SKILL.md). Pastas de modelos do próprio
usuário entram em `config/vara.json > pastas.modelos_usuario`.

## 2. Arquitetura do ato

**Sentença** (os três modelos seguem exatamente esta ordem):

1. Relatório enxuto, aberto por "Trata-se de" e fechado por **"É o Relatório."** (item 3).
2. Situação processual que condiciona o julgamento, quando houver — v.g., suspensão por IRDR já
   superada: "De logo, ressalte-se que…", seguido de "Nesse contexto, não há óbice ao regular
   prosseguimento e julgamento do feito, porquanto…" (art. 927, III, do CPC).
3. Preliminares e prejudiciais, uma a uma, cada qual com o teste concreto e a **conclusão decisória
   em parágrafo próprio, negrito e sublinhado** ("Desse modo, afasto a prejudicial de coisa
   julgada."). Questões conhecidas de ofício entram aqui (no modelo 2, a exclusão da Alagoas
   Previdência do polo passivo de ação de militar da ativa).
4. Mérito, aberto por "No mérito, depreende-se dos autos que…" (a pretensão, em uma frase), seguido
   da **tese central em negrito e sublinhado** ("Ocorre que a alegação das preterições não encontra
   guarida, …").
5. Desenvolvimento: norma (transcrita no que decide), interpretação, argumento sistêmico,
   precedente vinculante (transcrito), ônus da prova e ausência concreta de prova.
6. Fecho da fundamentação: síntese conclusiva ("Desse modo, devido à inviabilidade de comprovação
   da preterição relatada, … revelando-se inviável o reconhecimento do direito pretendido.") e, se
   for o caso, a ressalva do entendimento do juízo com deferência ao precedente vinculante.
7. **"Diante do exposto, julgo …"** — curto, em negrito e sublinhado.
8. Sucumbência; comandos de cumprimento (sublinhados); "Com o trânsito em julgado, **arquivem-se os
   autos com a devida baixa**, independentemente de nova determinação."; **"P. R. I."**

**Decisão de liminar** (modelo 4): relatório de quatro ou cinco linhas ("Trata-se de Mandado de
Segurança, com pedido de liminar, impetrado por … contra ato … imputado à …"; "Afirma que …";
"Pugna pela concessão de medida liminar para …"; "Anexou documentos às fls. …"; "Custas iniciais
pagas (fls. …)."; "É o Relatório." — o modelo grafa "relatório" com minúscula; padronize pela
sentença); requisitos da medida (norma de regência); fato com as fls.;
probabilidade do direito com a súmula ou o precedente que a sustenta; perigo da demora concreto;
o pedido que não prospera e por quê (no modelo, o pedido preventivo genérico contra apreensões
futuras); "Diante do exposto, defiro, em parte, a liminar requerida para …"; "Serve a presente
decisão como mandado."; comandos (notificação da autoridade para informações em 10 dias, ciência ao
órgão de representação judicial, vista ao Ministério Público, conclusão para sentença);
"Cumpra-se."

**Despacho**: sem relatório; os comandos encadeados até o próximo ato útil, com o gatilho final
("decorridos os prazos, voltem conclusos para sentença"); "Cumpra-se."

## 3. Relatório — enxuto, um evento por frase

Os modelos relatam em cinco a nove frases curtas o que a sentença precisa: quem pede, contra quem,
o quê e com base em quê; o que decidiu a liminar; o que a defesa arguiu (preliminares e linha do
mérito, separadas); réplica; parecer do Ministério Público; fato superveniente. Moldes da unidade:

- "Trata-se de Ação Ordinária proposta por **Nome Completo**, qualificado, em face do **Estado de
  Alagoas**." (classe "Ação Ordinária" nas ações de conhecimento; MS, ACP, Ação Popular e
  Desapropriação conservam o nome; partes em negrito, nunca abreviadas, sem caixa alta).
- Situação do autor e pretensão, no presente: "O autor, militar da ativa, recebe remuneração da
  graduação de Subtenente…"; "Nesta ação, com base unicamente no interstício mínimo …, busca o
  reconhecimento do direito à promoção …"; "Em síntese, busca o autor, …".
- Pedidos: em síntese fiel, na mesma frase da pretensão; havendo pedidos autônomos (três ou mais),
  "Ao final, requer: i) …; ii) …; iii) …", em romanos minúsculos. Tutela de urgência pedida: diga
  o que se pediu, em uma oração. Sem transcrição literal da inicial.
- Eventos, um por frase, no passado ou em frase nominal: "Indeferida a tutela antecipada e deferido
  o pleito de gratuidade de justiça em decisão às fls. 52/56."; "O Estado de Alagoas apresentou
  contestação às fls. 65/79. Preliminarmente, alegou coisa julgada … e impugnou a gratuidade da
  justiça. No mérito, defendeu, em síntese, a falta dos requisitos …"; "Réplica às fls. 102/113.";
  "O Ministério Público opinou pela improcedência do pedido (fls. 118/120)."; "O processo foi
  suspenso para aguardar o julgamento do Incidente de Resolução de Demandas Repetitivas n.º …".
- Fato superveniente que decide (modelo 2): "O autor comunicou ter sido promovido à graduação de 1º
  Sargento no curso da ação, em 03/02/2026, e reforçou o pedido … (fls. 118/122)." — a data só vai
  ao relatório quando é o próprio fato a decidir.
- Documentos: "Anexou documentos às fls. 10/32." (opcional nas sentenças).
- Audiência: uma frase, com as fls. do termo; o que nela se disse vai à fundamentação.

Nada de datas de protocolo, inventário de documentos, resumo tópico a tópico das peças nem trechos
transcritos. Cada frase leva as fls.

## 4. Fundamentação — perfil de análise

O juízo **resolve cada questão pelo dado concreto dos autos e pela norma aplicável, e diz a
conclusão antes de passar adiante**. Os modelos mostram o método em cada tipo de questão:

- **Coisa julgada**: compara objeto e causa de pedir das duas ações, com datas e números ("Naqueles
  autos, o autor buscou a promoção a Capitão a contar de 2020. Nesta, busca a mesma promoção, mas com
  base em preterição ocorrida no ano de 2023."), e conclui.
- **Impugnação à gratuidade**: renda concreta, com as fls., confrontada com o salário mínimo da
  época ("a holerite de janeiro de 2024 (fls. 50) aponta remuneração líquida de R$ 4.908,00. Isso
  equivalia a pouco mais de três salários mínimos à época…" — com as correções do item 9: "o
  holerite", "fl. 50"), e a falta de fato novo deduzido pelo
  impugnante. Benefício já indeferido e custas pagas: a impugnação é "inócua" (modelo 2).
- **Prescrição**: transcreve a tese vinculante, explica a distinção que ela traça (ato comissivo:
  cinco anos da publicação; ato omissivo: trato sucessivo) e enquadra cada pedido do caso numa das
  hipóteses, com as datas (modelo 3: promoções revistas de 2020 e 2024 — sem prescrição; promoções
  nunca concedidas — omissão, sem prescrição).
- **Litisconsórcio, legitimidade e outras questões de ordem pública**: aplica a tese ou a norma e
  afasta em uma frase impessoal ("Afasta-se, portanto, a obrigatoriedade de citação …"), ou decide
  de ofício com a razão de fato ("como o autor é militar da ativa, não há razão para atrair … a
  Alagoas Previdência, entidade que remunera somente os servidores inativos").
- **Mérito**: (i) a pretensão em uma frase; (ii) a tese central em negrito e sublinhado; (iii) a
  norma transcrita no que decide; (iv) a interpretação ("O interstício é o tempo mínimo em cada posto
  ou graduação, no entanto, a parte autora interpreta o regramento castrense como se tratasse de prazo
  máximo…"); (v) o argumento sistêmico (carreira, vagas, isonomia); (vi) o precedente vinculante
  transcrito, com o realce do trecho que decide ("grifos aditados"); (vii) o ônus da prova (art. 373,
  I, do CPC); (viii) o que concretamente falta nos autos ("não há nos autos qualquer documento que
  comprove a presença conjunta de todos os requisitos em época própria, quais sejam …"); (ix) a
  conclusão.
- **Precedente vinculante com ressalva**: o juízo aplica a tese e consigna, em um parágrafo, que
  dela diverge ("não obstante as ressalvas deste Juízo acerca desta questão"). Isso preserva a
  coerência do juízo sem desobedecer ao art. 927 do CPC.
- **Liminar**: requisito a requisito, com o fato e a fonte de cada um; o pedido que não cabe é
  enfrentado em parágrafo próprio, com a razão processual (no modelo, a inexistência de ato concreto
  ou iminente para o pedido preventivo).

Todo argumento das partes é enfrentado; o que o juízo conhece de ofício aparece na ordem lógica
(pressupostos, condições da ação, prescrição) — os modelos não deixam questão sem resposta.

## 5. Retórica e linguagem

**Voz.** Argumentação impessoal ("depreende-se", "afasta-se", "impõe-se", "evidencia-se"); o juízo
fala de si na terceira pessoa ("este Juízo já decidiu", "as ressalvas deste Juízo"). A primeira
pessoa aparece só onde se decide: no dispositivo e nas conclusões decisórias de preliminar,
prejudicial ou incidente, em parágrafo próprio, negrito e sublinhado ("Desse modo, afasto…",
"Desse modo, rejeito…", "Desse modo, determino a exclusão…").

**Encadeamento.** Cada parágrafo abre por uma transição que recolhe o anterior. Repertório dos
modelos (varie; nenhum vira cacoete): "De logo, ressalte-se que", "Nesse contexto,", "Entrementes,
cumpre salientar que", "Tal compreensão reforça", "No que concerne à", "Relativamente à", "Já quanto
à", "Nesse aspecto,", "No mérito, depreende-se dos autos que", "Ocorre que", "Com efeito,", "Nesse
particular,", "Diga-se, por importante, nesta trilha, que", "Note-se", "É importante insistir que",
"Evidencia-se, assim,", "É preciso fixar que", "Por outro lado, não se pode esquecer", "Neste ponto,
convém evidenciar", "Na espécie, em verdade,", "Para além,", "Isso porque", "Todavia,", "Por fim,",
"Desse modo,". Também da unidade: outrossim, porquanto, não obstante, na hipótese dos autos.

**Recursos persuasivos** (um por questão, quando ajudam a entender — nunca em série):

- analogia que ilumina a lógica do instituto ("é impossível para um Juiz ser promovido para
  Desembargador sem a existência de vagas, ainda que faça todos os cursos na Escola Judicial");
- argumento *a fortiori* com interpelação ("Ora, se não é possível sequer a realização do curso
  acaso o militar não esteja na ordem de antiguidade, imagine a promoção.");
- redução ao absurdo e consequência sistêmica ("as ações judiciais, se providas, acabarão, estas
  sim, por criar a preterição");
- adjetivação firme e pontual ("conclusão inexorável", "vigas mestras do sistema"), usada uma vez,
  no ponto que a merece, e nunca para desqualificar a parte.

**Destaques.** Negrito no termo ou trecho que identifica a questão enfrentada, embutido na frase
("No que concerne à alegação de **coisa julgada**…"); negrito e sublinhado no parágrafo que decide
(conclusões e tese central) e no dispositivo; sublinhado nos comandos e na cautela que o
destinatário não pode perder ("com a exigibilidade suspensa em razão da gratuidade"); nas
transcrições, negrito ou sublinhado no trecho que decide, com "(grifos aditados)" ao fim. Itálico só
para palavras latinas ou estrangeiras (*per saltum*, *mandamus*, *fumus boni iuris*, *verbis*).

**Transcrições.** Norma, tese vinculante, súmula transcrita isoladamente e ementa vão em bloco
(Courier New 10, recuo de 4 cm, espaçamento simples), qualquer que seja a extensão — é assim que os
modelos dão autoridade ao texto normativo. Trecho curto de peça ou de doutrina integrado à frase vai
entre aspas. Introduza o bloco por frase que diga o que ele prova ("o Tribunal rejeitou a hipótese
em sua tese n.º 3, que diz:") e, depois dele, retome com a aplicação ao caso.

## 6. Objetividade sem perda de enfrentamento

Os modelos são o padrão; a redação da minuta é **mais enxuta** do que eles. A régua é uma só: cada
parágrafo tem de ser necessário à conclusão, e nada que responda a pedido, argumento, prova ou
questão de ofício sai. O que se corta nos modelos ao adaptá-los:

| Nos modelos | Na minuta |
|---|---|
| Lista de quatro julgados do TJAL no mesmo sentido | o precedente mais pertinente, com a tese que decide (e o vinculante, se houver) |
| Art. 20 da Lei n.º 6.514/2004 transcrito com todos os incisos, alíneas e a tabela de interstícios | o *caput* e o inciso que decide o caso (v.g., o VI, do curso), com a alínea da graduação do autor |
| A mesma ideia dita duas vezes ("deveriam estar … minuciosamente explicadas" e "devem ser minuciosamente explicadas e comprovadas") | uma vez, no ponto em que conclui |
| Três analogias para a mesma tese (juiz e desembargador, o "Quinto" da lista de antiguidade dos juízes, embaixadores e promotores) | uma |
| Digressão sem função decisória ("A legislação estadual nesta matéria carece de atualização…") | suprimir, salvo se fundamentar algo do caso |
| Precedente de caso isolado do próprio juízo ("Este Juízo já decidiu, em um específico caso…") | só quando a distinção for necessária para tratar igualmente casos iguais |
| Ementa longa de tribunal de outro Estado (TJPR, no modelo 4) | precedente do STF, do STJ ou do TJAL, conferido; ementa só no trecho que decide |

Exemplo de enxugamento (modelo 1, dois parágrafos → dois mais curtos e completos):

> Modelo: "Ocorre que a alegação das preterições não encontra guarida, posto que baseadas tão somente
> no transcurso do tempo mínimo em cada posto ou graduação, com desconsideração aos demais requisitos
> legais para a ascensão na carreira militar. / O interstício é o tempo mínimo em cada posto ou
> graduação, no entanto, a parte autora interpreta o regramento castrense como se tratasse de prazo
> máximo, ao término do qual a promoção prescindiria do cumprimento das outras exigências legais."
>
> Minuta: "!! Ocorre que a alegação de preterição não encontra guarida, porquanto se apoia tão
> somente no decurso do tempo mínimo na graduação, com desconsideração dos demais requisitos legais."
> / "O interstício é prazo mínimo, e não máximo. Cumprido, habilita o militar a concorrer à promoção,
> sem dispensar o curso, a aptidão física, a inspeção de saúde e o comportamento exigidos pelo art.
> 20 da Lei Estadual n.º 6.514/2004."

Referência de extensão (o verificador aponta quando se passa dela): sentença até ~2.200 palavras,
decisão até ~1.300, despacho até ~450, incluídas as transcrições. Questão complexa pode exceder,
desde que o excesso seja enfrentamento, não repetição.

## 7. Dispositivo, sucumbência, comandos e fecho

- **Sentença**: "Diante do exposto, julgo improcedente a demanda." / "… julgo procedente a demanda
  para …" / "… julgo parcialmente procedente a demanda tão somente para …" — parágrafo inteiro em
  negrito e sublinhado (o gerador aplica). Contra a Fazenda, a sujeição ou não à remessa necessária
  (art. 496 do CPC) e os consectários de cada período (módulo de Fazenda Pública).
- **Sucumbência** (molde do modelo): "Condeno a parte autora nas custas e ao pagamento de honorários
  advocatícios, os quais fixo em R$ 1.000,00 (um mil reais), nos termos do art. 85, § 8º, do CPC.
  Todavia, a verba ficará sob condição suspensiva de exigibilidade, por ser a parte beneficiária da
  gratuidade da justiça, nos termos do art. 98, § 3º, do CPC." — a equidade do § 8º só quando o
  proveito econômico for inestimável ou irrisório ou o valor da causa muito baixo (Tema 1.076/STJ,
  conferido na Fase 2); nos demais casos, o percentual mínimo da faixa do § 3º, com a base de
  cálculo; o Estado é isento de custas, mas reembolsa as despesas antecipadas.
- **Comandos** em parágrafos próprios, sublinhados, no imperativo impessoal, como nos modelos:
  "Retire-se a suspensão do feito."; "Intime-se a parte impetrada para que cumpra imediatamente esta
  decisão, ficando, desde já, notificada a prestar as informações que julgar necessárias, no prazo de
  10 (dez) dias."; "Intime-se, ainda, a representação judicial do Estado de Alagoas para que …";
  "Após, dê-se vista ao Ministério Público por 10 (dez) dias."; "Em seguida, tornem os autos
  conclusos para sentença.". Se a configuração pedir (`redacao.abertura_comando`), o parágrafo abre
  por "À SPU,". Não se comanda o que a serventia faz de ofício (`cgj_normas.md`).
- **Fecho**: sentença — arquivamento e "P. R. I."; decisão e despacho — "Cumpra-se.". Local, data e
  assinatura vêm do modelo do SAJ e não entram na minuta.

## 8. Formatação (medida nos modelos; o gerador aplica)

A4; margens laterais de 3,32 cm e verticais de 2,54 cm; Times New Roman 12; recuo de 2,5 cm na
primeira linha; entrelinhas 1,5; 2 pt antes e depois; justificado. Transcrições: Courier New 10,
recuo esquerdo de 4 cm, espaçamento simples, justificadas. **Sem numeração de parágrafos**: nos
modelos ela é automática do editor, e o usuário a aplica no SAJ ao lançar a minuta.

## 9. Vícios dos modelos que não se reproduzem

- Erros de digitação e de regência: "promoação"; "lastreadas basicamente um dos pré-requisitos"
  (falta o "em"); "A conclusão inexorável que se chega" (é "a que se chega"); "O Estado Alagoas";
  "opinou improcedência" (é "opinou pela improcedência"); "neste caso,especificamente".
- Concordância: "Jose Alberto …, qualificada" (é "qualificado"); "a holerite" (é "o holerite").
- "posto que" com valor causal (é concessiva): use "porquanto", "uma vez que".
- Crase e números: "à fls. 121" (é "à fl. 121" ou "às fls."); "nº", "n." e "n°" (é "n.º");
  "§8º" (é "§ 8º"); "art. 19 e 20" (é "arts. 19 e 20"); "6(seis)" (é "6 (seis)").
- Maiúsculas indevidas no meio da frase: "Decisão", "Acórdão", "Curso", "Edital", "Sentença".
- Numeração inconsistente do mesmo incidente ("/5000" e "/50000"): confira nos autos e uniformize.
- Precedente citado de memória ou de tribunal sem relação com o caso; ementa sem dados completos.
- Gerúndios em série ("cabendo…", "aplicando…", "indeferindo…"): prefira a oração desenvolvida.
- Transcrição de trecho que não decide (incisos e alíneas alheios ao caso).

## 10. Regras anteriores ajustadas aos modelos (08/10/2026)

Por instrução do usuário, os modelos prevalecem sobre as regras anteriores da skill em estrutura,
análise e estilo. Ficou assim:

1. Parágrafos **sem numeração** (antes: "1.", "2."…).
2. Relatório em **síntese**: pretensão e pedidos resumidos com fidelidade, sem transcrição literal
   obrigatória; "Com a inicial, vieram os documentos…" passou a opcional; frase nominal admitida
   para evento processual ("Réplica às fls. …"); presente admitido para a pretensão da inicial.
3. Conclusão de preliminar, prejudicial ou incidente em **parágrafo decisório próprio**, negrito e
   sublinhado, com a primeira pessoa admitida ("Desse modo, afasto…"); a argumentação segue
   impessoal.
4. Norma, tese, súmula e ementa **em bloco**, qualquer que seja a extensão.
5. Fecho da sentença **"P. R. I."**; comandos no **imperativo impessoal**, sublinhados, sem
   "À SPU," (que volta se `redacao.abertura_comando` for preenchido).

Permanecem: vocabulário vedado, grafia de siglas, sem caixa alta indevida, sem títulos internos,
sem linguagem de método, travessão e dois-pontos só quando essenciais, parágrafos curtos, gerúndio
evitado, verificação de todo precedente, enfrentamento de todos os argumentos.
