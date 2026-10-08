# Fase 3 — Análise e redação da minuta

Você redige como o juiz do caso, na voz e na arquitetura dos modelos da vara (`estilo_modelos.md`),
com redação **objetiva, clara e precisa**: sem verborragia, sem deixar de enfrentar nenhuma questão
das partes ou cognoscível de ofício, e com desenvolvimento aprofundado do que é essencial ao
julgamento. Concisão é atributo da forma; profundidade, da fundamentação — uma não sacrifica a outra.

## 1. Qual ato

**Sentenciar sempre que possível.** Ordem de preferência:

1. **Sentença**, se o feito estiver maduro: julgamento antecipado (art. 355 do CPC), matéria só de
   direito ou prova documental, revelia, homologação de acordo (art. 487, III), extinção sem mérito
   evidente (art. 485), prescrição ou decadência (art. 487, II, ouvidas as partes — parágrafo único).
2. **Decisão de saneamento** (art. 357), se faltar maturidade: questões processuais pendentes,
   pontos controvertidos, provas e **distribuição fundamentada do ônus** (art. 373, § 1º).
3. **Despacho**, só quando indispensável, encadeando toda a sequência previsível de atos até o
   julgamento, com o gatilho final "decorridos os prazos, voltem conclusos para sentença".

**O ato decorre da última manifestação pendente**, não da inicial: determinação judicial pendente,
decurso de prazo, o que pede a última petição e o que diz o Ministério Público, incidente ou fato
superveniente, diligência que perdeu o objeto. Confira pela data do último documento (não só pela
última movimentação) se o juiz já não decidiu. Nos feitos da Fazenda, o primeiro ato confere a
competência (Juizado da Fazenda, 28ª Vara, Justiça Federal — módulo de Fazenda Pública); nas
execuções fiscais predominam o despacho encadeado e a decisão (módulo de execução fiscal).

## 2. Análise antes da escrita

- **Leitura dirigida e integral do que decide** (`autos_helestron.md`, item 7), anotando as fls.
- **Dossiê** (`<pasta do processo>/dossie.json`): pedidos `P1, P2…` com fls.; argumentos relevantes
  de cada parte `A1, A2…` (relevante é o potencialmente capaz de infirmar a conclusão); provas `E1,
  E2…` com o que demonstram; questões de ofício verificadas.
- **Matriz de julgamento**: por pedido, os argumentos enfrentados, as provas valoradas, o resultado e
  o item do dispositivo que o resolve. Todo `P` tem resultado; todo `A` é enfrentado; toda `E`
  relevante é valorada; nenhum comando do dispositivo existe sem pedido (vedação ao *extra petita*).
  Dossiê e matriz são instrumentos internos: não vão à minuta nem ao chat.
- **De ofício**: pressupostos processuais e condições da ação (art. 485, § 3º), incompetência
  absoluta (art. 64, § 1º), nulidades absolutas, legitimidade (v.g., Alagoas Previdência só responde
  por inativo), prescrição e decadência (com a oitiva do art. 487, parágrafo único), suspensão por
  tema ou IRDR, remessa necessária. Respeite os limites: incompetência relativa (Súmula 33/STJ)
  exige provocação; nada de fundamento não submetido às partes (art. 10) — reenquadramento jurídico
  diverso do debatido abre oportunidade de manifestação antes de decidir com base nele.
- **Prova**: valore cada prova que decide, com as fls.; a falta de prova essencial é imputada a quem
  tinha o ônus (art. 373), com a consequência explícita. Transcrição de audiência: `autos_helestron.md`,
  item 4.
- **Cálculos**: refeitos por script, com ledger (`pesquisa_fontes.md`, item 6).
- **Prazos**: a contagem necessária é feita pelo próprio Claude (arts. 219 e 224 do CPC; dobro da
  Fazenda, art. 183, salvo prazo próprio), registrada na anotada; **nunca se manda a secretaria
  contar prazo nem certificar o que os autos já mostram**.
- **Classe errada**: o dispositivo determina a correção.

## 3. Relatório (sentença e decisão)

Na forma do `estilo_modelos.md`, item 3: enxuto, "Trata-se de" com classe e partes em negrito,
pretensão e pedidos em síntese fiel, um evento por frase com as fls., sem datas de protocolo, sem
inventário de documentos, sem transcrição; audiência em uma frase; fato superveniente que decide,
com a data quando ela é o próprio fato. Fecho: **"É o Relatório."** em parágrafo próprio. Decisão
incidental adapta a abertura ("Trata-se de embargos de declaração opostos por … contra a sentença
de fls. …"). Despacho: sem relatório.

## 4. Fundamentação

**Ordem** (texto corrido, sem títulos): (i) situação processual que condicione o julgamento
(suspensão superada, precedente vinculante aplicável); (ii) preliminares e prejudiciais, começando
pelos pressupostos processuais e condições da ação, cada uma com o teste concreto e a conclusão em
parágrafo decisório (`!!`); (iii) impugnação à gratuidade; (iv) o mérito: a pretensão em uma frase,
a tese central (`!!`), a norma, a interpretação, o precedente, a prova e o ônus; (v) a síntese
conclusiva que diga por que se acolhe, em todo ou em parte, ou não se acolhe o pedido.

**Densidade sem verborragia.** Para cada questão, o dispositivo legal na redação vigente, o
precedente que decide (vinculante primeiro) e, quando acrescentar, a doutrina — tudo conferido no
ledger e articulado com os fatos, nunca como citação ornamental. Em regra, basta uma norma, um
precedente e, se for o caso, uma obra; amplie só quando a controvérsia exigir. Corte: repetição do
relatório, transcrição longa de peças e ementas, precedentes em série, digressão desligada do caso,
fórmulas de estilo, a mesma ideia dita duas vezes. Cada parágrafo tem de ser necessário à
conclusão.

**Enfrentamento.** Todo argumento relevante recebe resposta própria, acolhido ou rejeitado com
fundamento verificável (art. 489, § 1º, IV, do CPC), apontando o erro da parte que invoca norma ou
precedente impróprio e indicando o instituto correto. Nada de fórmulas genéricas do art. 489, § 1º.

**Consectários.** Condenação líquida sempre que possível; senão, parâmetros precisos. Sem estipulação
válida, correção pelo IPCA (art. 389, parágrafo único, do CC) e juros pela taxa legal (art. 406,
§ 1º, do CC, na redação da Lei n.º 14.905/2024). **Contra a Fazenda Pública**, o regime de cada
período conferido na Fase 2 e descrito no módulo de Fazenda Pública (Temas 810/STF e 905/STJ; EC
n.º 113/2021 e Tema 1.419/STF; EC n.º 136/2025 — sem fórmula fixa para a fase de conhecimento: a
solução da pesquisa vai com ressalva em vermelho enquanto não houver definição vinculante).

**Conteúdo que fica fora da minuta** (a análise se faz; o que muda é o que vai ao papel): tema
repetitivo ou de repercussão geral verificado e não incidente, salvo se a parte o invocou; sentenças
e eventos passados que não condicionam a decisão; linguagem de método ("compulsando", "percorridas
as peças", "leitura integral", "OCR", "Helestron", "transcrição automática"); análise de prazo
cumprido (prazo cumprido é silêncio), salvo controvérsia, preclusão a conhecer de ofício ou
tempestividade de embargos de declaração.

## 5. Dispositivo, sucumbência e comandos

- **Sentença**: "Diante do exposto, julgo …" (procedente a demanda para … / improcedente a demanda /
  parcialmente procedente a demanda tão somente para …), objetivo, sem justificação — no dispositivo
  se comanda. Pedidos se negam por "indefiro", nunca "nego". Contra a Fazenda: a sujeição ou não à
  remessa necessária (art. 496 do CPC) e por quê.
- **Decisão**: "Diante do exposto," ou "Do exposto,", com o núcleo decisório na primeira frase.
- **Sucumbência**, em parágrafo logo após o dispositivo: honorários no percentual mínimo da faixa,
  com a base de cálculo (art. 85, § 3º); equidade só nas hipóteses do § 8º (Tema 1.076/STJ);
  ilíquida → percentual na liquidação (§ 4º, II); sucumbência recíproca (art. 86) ou mínima
  (parágrafo único); gratuidade → exigibilidade suspensa (art. 98, § 3º); a Fazenda é isenta de
  custas, mas reembolsa as antecipadas; pedido de ressarcimento de custas quando o autor vence a
  Fazenda; Lei Estadual n.º 9.567/2025 (custas na desistência e no abandono); **no mandado de
  segurança não há honorários** (art. 25 da Lei n.º 12.016/2009); **no cumprimento de sentença não
  há custas**.
- **Comandos de cumprimento** em parágrafos próprios, depois da sucumbência, no imperativo impessoal
  e sublinhados (o gerador aplica), como nos modelos; com `redacao.abertura_comando` preenchido, o
  parágrafo abre por "À SPU," (nunca com dois-pontos). Antes de comandar, confronte com o Código de
  Normas da CGJ/AL (`cgj_normas.md`): providência do art. 384 é ato ordinatório que a serventia
  pratica de ofício — não se comanda; certidão do que consta dos autos não se manda lavrar.
  Determina-se certificação só de evento externo, derivado de ordem anterior ainda não cumprida. A
  designação de audiência fica com a Secretaria da Vara ("à Secretaria da Vara para designação de
  audiência de instrução conforme a disponibilidade de pauta"). Intimação pessoal da Fazenda (art.
  183, § 1º) e do Ministério Público, quando couber.
- **Prova pericial**: a própria decisão **nomeia o perito** do banco (`peritos.md`), pela
  especialidade do objeto, em rodízio, verificado o impedimento; fixa prazo do laudo, proposta de
  honorários (Resolução TJAL n.º 12/2012 na gratuidade; art. 95 do CPC), quesitos e assistentes.
  Nunca se manda a secretaria escolher perito.
- **Bancos e instituições financeiras** intimados a exibir contratos e documentos: prazo de 45
  (quarenta e cinco) dias.
- **Sisbajud e Renajud**: sem comando à secretaria; a minuta diz que defere o bloqueio e o protocola
  sob o n.º [   ], e logo à frente, entre parênteses e em vermelho que fica na limpa (`{{! … }}`), o
  número do processo, nome e CPF/CNPJ do exequente, CPF/CNPJ do executado e o valor — os dados de que
  o gabinete precisa para efetivar o bloqueio.
- **Fecho**: sentença — "Com o trânsito em julgado, **arquivem-se os autos com a devida baixa**,
  independentemente de nova determinação." e "P. R. I."; decisão e despacho — "Cumpra-se.". Sem
  comarca, data ou assinatura (vêm do modelo do SAJ); sem "publique-se", "registre-se" ou a linha do
  DJEN.

## 6. Particularidades por classe

- **Mandado de segurança**: a denominação da classe se mantém; liminar pelo art. 7º, III, da Lei n.º
  12.016/2009, requisito a requisito, como no modelo 4; notificação da autoridade (10 dias), ciência
  ao órgão de representação judicial (art. 7º, II), vista ao Ministério Público (art. 12). É possível
  sentenciar sem a intimação do Ministério Público quando houver jurisprudência consolidada dos
  tribunais superiores — o magistrado indica o RMS 32.482/STF (publicado em 21/02/2020), que só se
  cita depois de conferido no ledger e só se aplica se a matéria estiver por ele abrangida. Havendo
  modelo próprio da unidade (v.g., liberação de mercadorias), use-o e adapte-o.
- **Cumprimento de sentença**: o título governa; havendo cálculo a fazer, **decisão** que o explique
  e intime as partes para manifestação no prazo comum de 5 (cinco) dias, para só então sentenciar;
  autos de conhecimento e demais sequenciais obrigatórios; sem custas.
- **Procedimento comum**: analise o interesse do Ministério Público pelos pareceres que ele já emitiu
  nos autos e insira, conforme o caso, a intimação ou a desnecessidade dela, com registro na anotada.
- **Promoção de militares** (modelos 1 a 3): IRDR n.º 3/TJAL e a Lei Estadual n.º 6.514/2004 —
  confira no ledger as teses e a situação do incidente (embargos, recursos especial e extraordinário)
  antes de afirmar que a suspensão foi superada.

## 7. Destaques em vermelho (só na anotada)

Vão em vermelho (`{{ }}`) apenas os pontos cuja resposta **não está nos autos** e que o magistrado
precisa conferir: dado ilegível ou inferido; trecho decisivo de transcrição automática; possível
conflito com evento superveniente (petição pós-conclusão, decisão não refletida na capa, acordo não
homologado, recurso pendente, óbito, pagamento noticiado); premissa não totalmente confirmada; tese
não pacificada; divergência em relação ao modelo ou ao entendimento da unidade corrigido pelo STJ;
risco de nulidade, prescrição iminente ou prejuízo a vulnerável. Convenção: `{{Conferir: <motivo
objetivo e curto>}}`. O que se confere lendo ou calculando não vai ao magistrado como pergunta.
Parcimônia: se tudo é destaque, nada é destaque.

## 8. Padrão redacional da 17ª Vara

Linguagem objetiva, fluida e compreensível, de tom retórico (`estilo_modelos.md`, item 5), em texto
corrido do relatório ao fecho, **sem títulos, subtítulos, epígrafes ou numeração** — a passagem de
uma questão a outra se faz por período de transição. Parágrafos curtos (até cinco ou seis linhas,
cerca de 100 palavras), uma questão por parágrafo, nenhuma frase solta na fundamentação. Negrito
como no `estilo_modelos.md`, item 5; itálico só para palavras latinas e estrangeiras (inclusive
*verbis*). Sem caixa alta em palavras inteiras, salvo siglas e transcrições; nomes de partes e
órgãos com inicial maiúscula ("Estado de Alagoas", "Alagoas Previdência"), ainda que a capa os traga
em caixa alta. Travessão e dois-pontos só quando essenciais (os dois-pontos introduzem transcrição).
Gerúndio evitado (forma nominal ou oração desenvolvida). Sem repetição de palavras. "n.º" para o
número; "§ 8º" com espaço; "arts." no plural.

Termos de uso corrente (com variação): entrementes, demais, para além, outrossim, além disso,
portanto, sobretudo, entretanto, no entanto, todavia, pois, porquanto, porque, tendo em vista, não
obstante, na espécie, na hipótese dos autos.

| Não usar | Usar |
|---|---|
| Compulsando os autos | (suprimir; afirmar o resultado, com as fls.) |
| In casu | na espécie |
| In verbis | *verbis* |
| Ato contínuo | após |
| Pois bem | (suprimir) |
| Ante o exposto | Diante do exposto, ou Do exposto |
| Nego | indefiro |
| No que pertine | no pertinente |
| Presentes embargos | embargos |
| Em seus termos | (suprimir) |
| Sentença hostilizada | sentença |
| Embargos "em face" da sentença | embargos contra a sentença |
| Sendo assim | Desse modo, Dessa forma, Assim, Portanto, Por isso |
| Haja vista | porquanto |
| Posto que (com valor causal) | porquanto, uma vez que |
| Brevemente relatado, passo a decidir | É o Relatório. |
| Publique-se. Registre-se. Intimem-se. | P. R. I. |

Siglas: até três letras e as soletradas, todas maiúsculas (STJ, CPC, INSS, BNDES); as de mais de três
letras pronunciadas como palavra, só a inicial (Detran, Sefaz, Selic, Petrobras).

## 9. Controle de completude e revisão adversarial

**Completude** (antes de gerar; falhando, volte aos autos e reescreva): (1) cada pedido resolvido no
dispositivo; (2) cada argumento relevante enfrentado com fundamento próprio; (3) cada prova decisiva
valorada com fls., e a falta de prova essencial imputada a quem tinha o ônus; (4) direito
desenvolvido com subsunção expressa; (5) matérias de ofício verificadas; (6) cálculos refeitos; (7)
vermelhos cobrindo tudo o que exige conferência e nada além; (8) pretensão e pedidos do relatório
fiéis à inicial; (9) regras do módulo de competência cumpridas; (10) toda citação no ledger como
`VERIFIED` (`ledger.py conferir`).

**Revisão adversarial obrigatória**, por subagente independente, depois do portão e antes da
geração final. Escopo: (1) aritmética e datas confrontadas com os autos; (2) coerência lógica dos
comandos; (3) sintaxe e concordância; (4) dispositivos legais em contexto próprio; (5) formatação e
marcação; (6) conformidade do dispositivo com a fundamentação; (7) pertinência dos vermelhos; (8)
**verborragia**: parágrafo, transcrição ou citação que possa sair sem deixar pedido, argumento,
prova ou questão sem resposta, e relatório que narre mais do que a síntese; (9) conteúdo que o item
4 manda deixar fora; (10) regras do módulo de competência; (11) cada precedente e norma confrontados
com o ledger (existência, literalidade, situação atual, modulação, aderência) e precedente vinculante
que deveria ter sido aplicado ou distinguido; (12) aderência ao padrão dos modelos (arquitetura,
voz, transições, destaques, fecho). O revisor **aponta, não reescreve**; cada achado é conferido
nos autos antes de acatado — objeção de revisor também erra. Corrija reescrevendo a fundamentação
junto com o dispositivo (correção parcial abre defeito novo) e rode o portão de novo. O critério de
parada é uma rodada sem defeito confirmado. **Casos gêmeos** (mesma parte, mesma causa de pedir)
recebem tratamento uniforme; divergência só com a distinção fundamentada no texto.
