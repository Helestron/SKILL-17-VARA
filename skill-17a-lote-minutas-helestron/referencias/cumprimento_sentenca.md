# Módulo Cumprimento de Sentença contra a Fazenda Pública — 17ª Vara Cível da Capital

Orienta a análise e a redação dos cumprimentos de sentença da vara (Estado de Alagoas, Alagoas
Previdência e demais entes). Marcas: **[modelo]** = consta de ato do próprio juízo (`modelos/despacho_CS_*`)
e indica a praxe da unidade, mas a norma ou o precedente **só se cita depois de conferido na Fase 2**
(ledger `VERIFIED`); **[conferir]** = dado a pesquisar no caso. As regras de redação (`redacao.md`,
`estilo_modelos.md`) e o módulo de Fazenda Pública (consectários, RPV, honorários) valem integralmente.

## 1. Quando se aplica e o que ler antes

- Classe "Cumprimento de Sentença" ou "Cumprimento de Sentença contra a Fazenda Pública", em incidente
  (`<número>-01`, `-02`…, que o SAJ exibe como `/01`) ou nos próprios autos de conhecimento — a capa
  pode trazer "Procedimento Comum Cível" com o processo já na fase de cumprimento: decida pela fase
  real (movimentações e última manifestação), não pelo nome da classe.
- **O título governa** (`redacao.md`, item 6; `pesquisa_fontes.md`, item 6): leia a sentença, o acórdão e
  a certidão de trânsito nos autos de conhecimento antes de qualquer peça do cumprimento. O inventário
  aponta os autos relacionados (`autos.py relacionados N`) e avisa quando faltam ("AUTOS DE ORIGEM
  AUSENTES": peça ao usuário que os baixe pelo Helestron e marque em vermelho o que deles depender).
- `autos.py requisitos N -t "<T>"` dá, com as fls., as pistas de cada requisito (item 3), da
  sucessão, da impugnação, do requisitório e da cessão, no processo e nos relacionados. Pista não é
  prova: confirme lendo as fls.

## 2. Fase do processo e ato de cada uma

| Situação nos autos (última manifestação pendente) | Ato | Modelo |
|---|---|---|
| Requerimento sem algum requisito do art. 534 do CPC e da Resolução TJAL n.º 21/2023 | despacho de adequação, que enumera **só o que falta**, sob pena de extinção sem resolução do mérito, e já encadeia a intimação da Fazenda | `despacho_CS_adequar_requerimento_art534_Res21-2023_espolio_sem_inventariante` |
| Requerimento completo | despacho de intimação da Fazenda para impugnar em 30 dias (art. 535), com descontos obrigatórios, contas para as retenções e, se houver, a habilitação; encadeia manifestação do exequente (15 dias) e conclusão | idem, parágrafos de encadeamento |
| Exequente falecido; pedido de habilitação | despacho que organiza a sucessão (item 5) | `despacho_CS_habilitacao_sem_inventario_…`; `despacho_CS_adequar_…` (item vi) |
| Exequente pede que o executado junte fichas financeiras | despacho que devolve o ônus ao exequente (item 4) | `despacho_CS_fichas_financeiras_onus_da_exequente` |
| Impugnação apresentada | manifestação do exequente; depois, **decisão** da impugnação; havendo cálculo a refazer, decisão que o explique e intime as partes em 5 dias antes de homologar | — |
| Sem impugnação, ou com concordância expressa da Fazenda | decisão que homologa o cálculo e determina a expedição do requisitório (item 7) | — |
| Requisitório expedido e pedido de cessão de crédito | despacho que remete o interessado à Presidência do TJAL e ordena à Secretaria que não torne os autos conclusos por petição repetitiva (item 8) | `despacho_CS_cessao_de_credito_…` |
| Pagamento comprovado | levantamento ou transferência e **sentença de extinção** (arts. 924, II, e 925 do CPC) | — |
| Obrigação de fazer (implantação em folha, apostilamento) | decisão com prazo e, se necessário, multa (arts. 536 e 537 do CPC) | — |

Despachos da fase de cumprimento remetem os autos à fila **"após Sentença"** do SAJ ("conclusos na
fila "após Sentença"") [modelo].

## 3. Requisitos do requerimento (art. 534 do CPC e Resolução TJAL n.º 21/2023 [modelo; conferir])

Confira um a um, com as fls., e peça no despacho de adequação **apenas o que faltar** — não se
determina juntar o que já está nos autos (CGJ/AL, `cgj_normas.md`):

1. **Demonstrativo discriminado e atualizado** do crédito (art. 534, *caput* e incisos I a VI): nome
   e CPF do exequente; índice de correção monetária; juros e taxa; termos inicial e final de juros e
   correção; periodicidade da capitalização, se houver; descontos obrigatórios — "observado o
   título executivo judicial", preferencialmente pelo programa de cálculos judiciais ProjefWeb
   [modelo]. Pluralidade de exequentes: demonstrativo próprio de cada um (art. 534, § 1º).
2. **Mais de um devedor**: a responsabilidade de cada um, com percentual e valor, conforme o título
   [modelo].
3. **Descontos obrigatórios**: contribuição previdenciária (com o órgão e o CNPJ), FGTS, imposto de
   renda (com o número de meses, no caso de rendimentos recebidos acumuladamente — art. 12-A da Lei n.º
   7.713/1988 [conferir]) e outras contribuições [modelo].
4. **Conta bancária** do credor originário e do advogado, para o depósito do requisitório [modelo].
5. **Contrato de honorários**, se o advogado quiser o destaque no requisitório (art. 22, § 4º, da Lei
   n.º 8.906/1994 [conferir]) [modelo].
6. **Sucessão**: falecido o credor, a prova do inventário (termo de inventariante, sentença ou
   escritura) ou a habilitação de todos os sucessores (item 5) [modelo].
7. **Título e trânsito**: sentença, acórdão e certidão de trânsito em julgado, nos autos de origem.
8. **Multa do art. 523, § 1º**: não se aplica à Fazenda (art. 534, § 2º) — cálculo que a inclui está
   errado nesse ponto.

## 4. Cálculos, fichas financeiras e Contadoria

- O cálculo é **ônus do exequente** (art. 534). Os dados de remuneração (fichas financeiras,
  contracheques) são de fácil obtenção pelo próprio servidor, por requerimento administrativo ou
  sistema eletrônico de consulta, e o encargo não se transfere ao executado [modelo]. Exceção a
  enfrentar quando invocada: dado em poder do executado que o exequente comprovadamente não obteve
  (requerimento negado ou não respondido) — o art. 524, §§ 3º a 5º, do CPC autoriza a requisição, com
  prazo [conferir a aplicação ao rito do art. 534].
- **Contadoria Judicial Unificada (CJU)**: não é cabível o encaminhamento quando há meio eletrônico
  apto ao cálculo (periodicidade, principal, juros e multa estão ao alcance de quem assiste o
  exequente) [modelo]. Se a parte invocar a gratuidade, enfrente o argumento com cuidado: o art. 98,
  § 1º, VII, do CPC inclui expressamente na gratuidade o custo da memória de cálculo exigida para a
  execução, de modo que a resposta depende do caso — meio eletrônico gratuito ao alcance da parte e
  orientação do STJ e do TJAL sobre a remessa à Contadoria do beneficiário da gratuidade [conferir] —,
  e a divergência com o modelo, se houver, vai em vermelho na anotada.
- **Refaça toda conta** no ledger (`pesquisa_fontes.md`, item 6): índices e juros de cada período
  conforme o título e o módulo de Fazenda Pública (Temas 810/STF e 905/STJ; EC n.º 113/2021; EC n.º
  136/2025); a multa do art. 523 excluída; descontos obrigatórios; honorários da fase (item 7).
- Título claro não se substitui por critério que se repute melhor; título obscuro interpreta-se, com
  as razões.

## 5. Sucessão do exequente falecido

- **Espólio** representa-se pelo **inventariante** (art. 75, VII, do CPC) e, antes da nomeação dele,
  pelo **administrador provisório** (arts. 613 e 614 do CPC; art. 1.797 do Código Civil) [conferir].
  Peticionar em nome do "Espólio de Fulano", qualificando-se como herdeiros, sem inventário,
  inventariante nem administrador provisório demonstrado, é irregularidade de representação, que se
  manda sanar (art. 76 do CPC) [modelo].
- **Inventário aberto**: o inventariante representa o espólio; junta o termo de compromisso.
  **Encerrado**: sucedem os herdeiros e legatários na forma da partilha (formal de partilha ou
  escritura). **Inexistente**: habilitação de **todos** os sucessores (arts. 687 a 692 do CPC
  [conferir]), com certidão de óbito, prova do parentesco e procurações.
- O crédito integra a herança; os descendentes concorrem com o **cônjuge sobrevivente** conforme o
  regime de bens (art. 1.829, I, do Código Civil), e o companheiro tem o mesmo regime sucessório do
  cônjuge (Tema 809/STF [conferir]). Habilitação **parcial**, só de parte dos herdeiros, não se defere:
  arriscaria pagamento ineficaz e lesão ao direito de quem não está nos autos [modelo].
- **Indicar o endereço** do herdeiro ou do cônjuge ausente é ônus dos requerentes: a alegação genérica
  de desconhecimento não basta, e os familiares têm melhores condições de localizá-lo do que o juízo
  [modelo]. Com o endereço, intima-se o interessado para, em 15 dias, manifestar-se e, querendo,
  habilitar-se; em seguida, vista à Fazenda [modelo].
- Argumento a enfrentar quando invocado: pagamento a dependentes habilitados sem inventário (Lei n.º
  6.858/1980) — confira na Fase 2 o alcance da lei e a orientação do STJ sobre créditos de servidor
  reconhecidos em juízo antes de aplicá-la ou afastá-la [conferir].
- A morte da parte suspende o processo até a habilitação (art. 313, I, do CPC [conferir]); a Fazenda
  se manifesta sobre a habilitação antes da decisão.

## 6. Impugnação (art. 535 do CPC)

- Prazo de 30 dias, próprio — sem o dobro do art. 183 (§ 2º) —, nos próprios autos.
- Matérias do art. 535, I a VI; causa modificativa ou extintiva só se superveniente ao trânsito.
- **Excesso de execução**: a Fazenda declara de imediato o valor que entende correto, sob pena de não
  conhecimento da arguição (art. 535, § 2º).
- **Parte incontroversa**: cumprimento imediato (art. 535, § 4º) — expede-se o requisitório do valor
  não impugnado.
- Na intimação para impugnar, a Fazenda se manifesta sobre os descontos obrigatórios informados pelo
  exequente (valor e percentual) e indica as contas para o depósito das retenções de imposto de renda
  e de contribuição previdenciária, sob pena de preclusão; e sobre a habilitação, se houver [modelo].
- Inexigibilidade fundada em decisão do STF (art. 535, §§ 5º a 8º) [conferir a modulação no caso].

## 7. Requisitórios e honorários

- **RPV ou precatório** conforme o valor por beneficiário (Lei Estadual n.º 7.154/2010 para o Estado
  de Alagoas — módulo de Fazenda Pública, item 5 [conferir]); o prazo de pagamento da RPV é o do art.
  535, § 3º, II, do CPC (dois meses da entrega da requisição), a confrontar com os 90 dias do art. 2º da
  Lei Estadual n.º 7.154/2010 [conferir, como no módulo de Fazenda Pública]; o precatório é requisitado
  ao Presidente do Tribunal (art. 535, § 3º, I; art. 100 da CF). Vedado fracionar o valor para enquadrá-lo como RPV (art. 100, § 8º, da CF);
  renúncia ao excedente só com poderes específicos [conferir].
- **Honorários contratuais**: destaque do principal com o contrato juntado antes da expedição (art. 22,
  § 4º, da Lei n.º 8.906/1994) [conferir]; o destaque segue a natureza do crédito principal, e a
  expedição de requisitório autônomo (RPV separada) para os honorários contratuais encontra limite na
  jurisprudência do STF [conferir antes de deferir].
- **Honorários sucumbenciais da fase de cumprimento**: não são devidos no cumprimento contra a Fazenda
  que enseje precatório, se não impugnado (art. 85, § 7º, do CPC), nem quando o crédito se paga por RPV
  e não houve impugnação (Tema 1.190/STJ [conferir]); ressalva-se a execução individual de sentença
  coletiva, em que são devidos ainda que não impugnada (Súmula 345/STJ e Tema 973/STJ [conferir]).
  Os honorários são verba de natureza alimentar, satisfeita por precatório ou RPV em ordem especial
  (SV 47 [conferir]); a execução autônoma dos honorários sucumbenciais, sem fracionar o crédito
  principal, é admitida pelo STF (Tema 18 da repercussão geral, RE 564.132 [conferir]).
- **No cumprimento de sentença não há custas** (`redacao.md`, item 5).
- A decisão que homologa o cálculo fixa o valor de cada beneficiário (principal, honorários
  contratuais destacados, honorários sucumbenciais), as retenções e a data-base, e determina a
  expedição; não manda a Secretaria "calcular" nem "certificar" o que os autos mostram.

## 8. Depois da expedição

- **Cessão de crédito** de precatório já expedido: a comunicação é feita pelo interessado diretamente
  à Presidência do Tribunal (art. 50 da Resolução TJAL n.º 17/2020 [modelo; conferir]) e ao ente
  devedor (art. 100, §§ 13 e 14, da CF; Resolução CNJ n.º 303/2019 [conferir]); não compete ao juízo da
  execução apreciá-la [modelo].
- **Petição repetitiva** sobre questão já decidida: reitera-se o despacho anterior e ordena-se à
  Secretaria que não torne os autos conclusos por mera petição de igual teor, certificando apenas a
  juntada [modelo]. Os autos permanecem arquivados, se for o caso, e os requerentes são intimados por
  seus advogados.
- **Sequestro** de verba de precatório é da Presidência do Tribunal (art. 100, § 6º, da CF), não da
  vara.
- **Pagamento**: levantamento por alvará eletrônico ou transferência (CGJ/AL, `cgj_normas.md`) e
  sentença de extinção pelo pagamento (arts. 924, II, e 925 do CPC), sem custas.

## 9. Redação dos despachos de cumprimento (padrão dos modelos)

- Abertura: "Trata-se de Cumprimento de Sentença proposto por **Fulano de Tal** em face do **Estado de
  Alagoas**, todos qualificados." — ou, no despacho que responde a petição isolada, a frase que a
  descreve ("Verifica-se que os exequentes voltaram a peticionar nos autos requerendo…") [modelo].
- Relatório de duas ou três frases e "É o Relatório." quando há questão a decidir (habilitação,
  representação); sem relatório no despacho de mero impulso.
- Fundamentação curta e suficiente: um a três parágrafos, com a norma e a razão de fato (quem tem o
  ônus, por que o pedido não se defere como formulado).
- Núcleo decisório: "Diante do exposto, determino a intimação da parte exequente para, no prazo de 15
  (quinze) dias, sob pena de extinção do processo sem resolução do mérito, trazer aos autos:" — e a
  enumeração recuada, `+ i)`, `+ ii)`… e `++ a)`, `++ b)`… (`formato_minuta.md`), só com o que falta.
  O parágrafo do dispositivo leva só a ordem (sai inteiro em negrito e sublinhado); a justificativa
  que um dos modelos põe depois dela ("A alegação genérica de desconhecimento do paradeiro não é
  suficiente…") vai no parágrafo anterior, na fundamentação.
- Encadeamento até o próximo ato útil, um comando por parágrafo, sublinhados: "Com a manifestação da
  parte exequente no prazo assinalado, intime-se a Alagoas Previdência para, no prazo de 30 (trinta)
  dias, querendo, impugnar o cumprimento de sentença, …"; "Após a impugnação, intime-se a parte
  exequente para que se manifeste no prazo de 15 (quinze) dias. Exaurido o prazo, conclusos na fila
  "após Sentença"."; "Não havendo impugnação ou havendo concordância expressa da Fazenda Pública com
  os cálculos da parte exequente, imediatamente conclusos na fila "após Sentença"."; "Decorrido o
  prazo fixado para a parte exequente sem o cumprimento da determinação, tornem os autos imediatamente
  conclusos." [modelo].
- Fecho: "Cumpra-se." — ou "Cumpra-se observada a sequência acima." quando o despacho encadeia
  vários atos [modelo].
- Sem numeração de parágrafos, **não se remete a "item 4"** do próprio ato (como faz o modelo de
  adequação): diga "a determinação acima" ou descreva o ato.
- Vícios dos modelos de cumprimento que não se reproduzem: "nº" (é "n.º"); "Despacho" com maiúscula
  no meio da frase; "verifica-se que os requerentes apresentaram-se" (com o "que", a próclise:
  "se apresentaram"); "a todo período" (é "a todo o período"); despacho que termina sem "Cumpra-se.".

## 10. Armadilhas próprias

- Minutar o cumprimento sem ler o título nos autos de conhecimento.
- Pedir no despacho de adequação o que já está nos autos, ou deixar de pedir o que falta (o despacho
  de adequação é um só e completo).
- Mandar a Contadoria fazer a conta que o exequente pode fazer por meio eletrônico; transferir ao
  executado o ônus das fichas financeiras sem prova de recusa.
- Aceitar "Espólio" sem inventariante; deferir habilitação parcial; ignorar o cônjuge ou o
  companheiro sobrevivente; não ouvir a Fazenda sobre a habilitação.
- Aplicar a multa do art. 523 à Fazenda; condenar em custas no cumprimento; fixar honorários da fase
  em cumprimento não impugnado, por precatório ou por RPV (salvo a execução individual de sentença
  coletiva).
- Fracionar o crédito para enquadrá-lo como RPV; esquecer o destaque dos honorários contratuais
  requerido com o contrato; expedir sem as retenções e contas informadas.
- Apreciar cessão de crédito de precatório já expedido, ou determinar sequestro de verba de precatório.
- Contar o prazo de impugnação em dobro (é próprio).
