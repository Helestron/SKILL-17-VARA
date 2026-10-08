# Módulo Fazenda Pública Estadual — 17ª Vara Cível da Capital (Maceió)

Este digesto orienta a análise dos feitos do Estado de Alagoas. **Nada daqui vai à minuta sem a
Fase 2** do SKILL.md (ledger `ledger.py`, entrada `VERIFIED`). Marcas: **[semente]** =
texto conferido em fonte oficial em 27/09/2026, que ainda assim entra no ledger do lote e é
reconferido se tiver mais de 30 dias; **[conferir]** = dado que não foi verificado e que depende
de pesquisa no caso. As regras de redação (`redacao.md`, `estilo_modelos.md`) valem integralmente e prevalecem sobre
este digesto no que toca a estilo, estrutura e fecho.

## 1. Competência da unidade e declínios

- **Competência**: feitos em que interessado o **Estado de Alagoas**, os entes de sua administração
  indireta e os delegatários dos serviços públicos que conceder ou permitir (lista oficial de
  unidades do TJAL, APMP, 16/08/2023, com base na Lei Estadual n.º 6.564/2005). A Capital tem outras
  varas da Fazenda Estadual (16ª, 18ª e 19ª): prevenção e conexão entre elas seguem o CPC.
- **Juizados Especiais da Fazenda Pública da Capital** (Lei Estadual n.º 9.203/2024, arts. 6º e 7º
  [semente]; Lei n.º 12.153/2009, art. 2º, competência absoluta onde instalado [semente]): causas de
  até 60 salários mínimos sobre multas de trânsito, ações indenizatórias e outras obrigações de fazer
  ou dar. **Ficam nas varas da Fazenda**, qualquer que seja o valor: demandas de **saúde** (art. 6º,
  § 1º); ações em que o Estado ou suas entidades sejam autores; sociedades de economia mista e
  delegatários; mandado de segurança, desapropriação, ação popular, improbidade, execução fiscal e
  direitos difusos ou coletivos; imóveis públicos; **tributos**, **concursos públicos**, **promoções de
  servidores civis e militares** e **previdenciário**; impugnação de demissão ou de sanção
  disciplinar; licitações e contratos; interesse de incapazes (art. 7º, § 3º). Obrigações vincendas:
  doze parcelas mais as vencidas (art. 7º, § 2º); complexidade técnica ou jurídica afasta o Juizado
  (art. 7º, § 1º). Processo de competência do Juizado na vara: declínio de ofício (art. 64, § 1º, do
  CPC). Regra de transição para feitos anteriores à instalação dos Juizados [conferir o ato do TJAL].
- **Criança ou adolescente no polo ativo** contra o Estado: art. 6º, § 2º, da Lei n.º 9.203/2024 atribui
  competência material absoluta à **28ª Vara Cível da Capital (Infância e Juventude)** [semente];
  confira o alcance do dispositivo (está na lei dos Juizados, com redação geral) e a prática da
  distribuição antes de declinar [conferir].
- **Justiça Federal**: União no polo (art. 109, I, da CF); medicamentos sem registro na ANVISA (Tema
  500/STF [semente]); medicamentos não incorporados e oncológicos com tratamento anual igual ou
  superior a 210 salários mínimos, nas ações ajuizadas após a publicação do resultado do julgamento de mérito (19/09/2024) (Tema 1.234/STF e SV 60
  [semente]; embargos julgados em 25/09/2026, acórdão por publicar: reconfira a tese).
- **Execuções fiscais estaduais**: a vara especializada de executivos fiscais da Capital é municipal
  (15ª); as estaduais correm nas varas da Fazenda Estadual [conferir na distribuição]. Use
  `referencias/execucao_fiscal.md`.

## 2. Partes, prerrogativas e ônus do processo

- **Representação**: Estado pela Procuradoria-Geral do Estado; autarquias e fundações pela própria
  procuradoria ou pela PGE, conforme a lei de cada ente [conferir nos autos]. Empresa estatal de
  direito privado não tem as prerrogativas da Fazenda, salvo regime de serviço público não
  concorrencial reconhecido pelo STF [conferir].
- **Prazo em dobro e intimação pessoal** (art. 183 do CPC [semente]), inclusive eletrônica; não há
  dobro quando a lei fixa prazo próprio (art. 183, § 2º), como os 30 dias do art. 535, nem no Juizado
  da Fazenda. O prazo da Fazenda corre da intimação pessoal registrada nos autos, não do DJEN.
- **Custas**: o Estado, suas autarquias e fundações de direito público são isentos (Lei Estadual n.º
  9.567/2025, art. 9º, I [semente]); vencido, reembolsa as despesas antecipadas pelo vencedor (art. 82,
  § 2º, do CPC). Abandono, desistência e transação não dispensam custas; a transação antes da
  sentença dispensa as remanescentes (art. 31 e § 1º [semente]).
- **Honorários contra a Fazenda**: faixas do art. 85, §§ 3º a 5º, e liquidação quando ilíquida
  (§ 4º, II) [semente]; equidade só nas hipóteses do § 8º (Tema 1.076/STJ [semente]; o Tema
  1.255/STF, sobre o mesmo ponto, estava sem tese em 27/09/2026); honorários recursais (§ 11). À
  Defensoria Pública são devidos também contra o Estado (Tema 1.002/STF [semente]; a Súmula 421/STJ
  está cancelada [semente]). No mandado de segurança não há honorários (art. 25 da Lei n.º 12.016/2009;
  Súmula 512/STF; Súmula 105/STJ [semente]).
- **Perícia**: a Fazenda sujeita-se ao depósito prévio dos honorários do perito que requerer (Súmula
  232/STJ [semente]); nomeação na própria decisão (`redacao.md`, item 5, e `peritos.md`).
- **Remessa necessária** (art. 496 [semente]): sentença contra o Estado, suas autarquias e fundações
  de direito público, salvo condenação ou proveito de valor certo e líquido inferior a **500 salários
  mínimos** (§ 3º, II) ou sentença fundada em súmula de tribunal superior, repetitivo, IRDR, IAC ou
  orientação vinculante do próprio ente (§ 4º). Sentença ilíquida não se beneficia do limite
  (Súmula 490/STJ [semente], editada sob o CPC/1973: confira a orientação atual do STJ [conferir]).
  A remessa devolve todas as parcelas, inclusive honorários (Súmula 325/STJ [semente]). A sentença
  diz se se sujeita ou não à remessa e por quê.
- **Tutela provisória contra a Fazenda**: art. 1.059 do CPC (remete à Lei n.º 8.437/1992, arts. 1º a
  4º, e ao art. 7º, § 2º, da Lei n.º 12.016/2009) [semente]; a ADI 4.296 declarou inconstitucionais o
  art. 7º, § 2º, e o art. 22, § 2º, da Lei n.º 12.016/2009 [semente]; execução provisória vedada nas
  hipóteses do art. 2º-B da Lei n.º 9.494/1997 [semente]. Multa cominatória contra a Fazenda
  (art. 537) e bloqueio de verbas em saúde com fundamentação (Tema 84/STJ [semente]).

## 3. Consectários — questão aberta desde a EC 136/2025 (pesquisa obrigatória em todo lote)

Separe os períodos e cite a norma e o precedente de cada um, conferidos:

1. **Até 08/12/2021**: Tema 810/STF e Tema 905/STJ [semente] — relação não tributária, correção pelo
   IPCA-E e juros da caderneta de poupança (art. 1º-F da Lei n.º 9.494/1997 [semente]); servidores e
   empregados públicos, com as faixas do Tema 905; relação tributária, os mesmos índices com que o
   Estado cobra seus créditos (Súmula 523/STJ [semente]: Selic se prevista na legislação local, sem
   cumulação). Títulos com índice diverso e normas supervenientes: Temas 1.170 e 1.361/STF [semente].
2. **Da EC 113/2021 até a EC 136/2025**: Selic única (art. 3º da EC 113/2021, redação original; Tema
   1.419/STF [semente]). Os embargos do Tema 1.419 (sessão de 8 a 15/05/2026) restringiram a tese a esse
   período, "não havendo projeção automática de seus efeitos ao novo regime" da EC 136/2025. O
   **Tema 1.457/STF** [semente, sem tese] discute o termo inicial da Selic nesse regime e o da mora:
   pendente em 27/09/2026, sem suspensão registrada; reconfira e, sem tese, marque em vermelho.
3. **Depois da EC 136/2025**: o art. 3º da EC 113/2021 passou a tratar dos **requisitórios da Fazenda
   federal** (IPCA mais juros simples de 2% ao ano desde a expedição, limitados à Selic; processos
   tributários pelos critérios do crédito tributário) [semente]; o art. 97, §§ 16 e 16-A, do ADCT
   aplica aos **requisitórios contra Estados e Municípios**, a partir de 1º/08/2025, IPCA mais juros
   simples de 2% ao ano **desde a expedição**, limitado à Selic [semente]. Para a **fase de
   conhecimento** da condenação do Estado (antes do requisitório), não há regra constitucional
   expressa: pesquise no lote — STF (ADI 7.873 e demais ações contra a EC 136/2025; temas novos),
   STJ (temas e afetações) e TJAL — e registre a solução com fonte. Sem definição vinculante, a
   minuta fundamenta a escolha (v.g., art. 1º-F da Lei n.º 9.494/1997 na leitura do Tema 810, ou
   arts. 389, parágrafo único, e 406 do CC na redação da Lei n.º 14.905/2024 [semente]) e marca a
   questão em vermelho na versão anotada, para decisão do magistrado; alternativa aceitável é fixar
   o marco e remeter os índices à liquidação "conforme a legislação e o entendimento vinculante
   vigentes", também com o vermelho.
4. **Termos iniciais**: juros desde a citação nas obrigações ilíquidas e nas remuneratórias (art. 240
   do CPC; nas obrigações ilíquidas devidas ao servidor, Tema 611/STJ [semente]); na responsabilidade extracontratual, verifique no STJ a aplicação da Súmula 54 à Fazenda
   [conferir]; correção do dano moral desde o arbitramento (Súmula 362/STJ) [conferir texto]; repetição
   de indébito tributário: correção desde o pagamento indevido (Súmula 162/STJ) e juros desde o
   trânsito (Súmula 188/STJ), afastados quando a lei local adotar a Selic (Súmula 523/STJ) [semente].

## 4. Matérias frequentes

- **Saúde** (sempre na vara, nunca no Juizado): Temas 6, 500, 793 e 1.234/STF; SV 60 e 61; Tema
  106/STJ [semente]. Roteiro de verificação, com fls.: registro na ANVISA; incorporação às listas do
  SUS; laudo fundamentado, com evidência científica de alto nível, e imprescindibilidade; ineficácia
  dos substitutos do SUS; incapacidade financeira; negativa administrativa e **análise judicial do
  ato de não incorporação e do indeferimento** (item IV da tese do Tema 1.234, sob pena de nulidade);
  competência e custeio (Tema 1.234 e SV 60); direcionamento do cumprimento ao ente responsável e
  ressarcimento (Tema 793); bloqueio de verbas como último recurso, fundamentado (Tema 84/STJ).
- **Servidores civis**: regime jurídico único (Lei Estadual n.º 5.247/1991, indexada no SAPL como
  "Lei Ordinária n.º 2, de 26/07/1991", norma 2457: confira no SAPL de Alagoas pelo número de
  indexação; há leis alteradoras, v.g., Lei n.º 8.391/2021 [conferir
  texto]); licença-prêmio: o art. 91, na redação da Lei n.º 6.043/1998, trata de afastamento para
  curso de capacitação, e a licença-prêmio por assiduidade é a redação original [semente] — confronte
  o período aquisitivo com esse marco e confira a eventual regra de transição; conversão em pecúnia e
  ônus da prova (IRDR Tema 5/TJAL [semente]); na Constituição Estadual, a conversão da licença especial
  em abono pecuniário (art. 49, IX) foi declarada inconstitucional na ADI 276 [semente: nota do texto
  compilado da ALE; confira o acórdão no portal do STF]; inativo: Tema 635/STF [semente; servidor ativo
  pendente]; prescrição da conversão contada da aposentadoria (Tema 516/STJ [semente]); servidor estabilizado pelo art. 19 do ADCT sem
  efetividade (Tema 1.157/STF [semente]); desvio de função (Súmula 378/STJ e Tema 14/STJ [semente]);
  vedação de aumento por isonomia (SV 37 [semente]); revisão geral anual (Tema 19/STF [semente]);
  contratação temporária nula (Tema 916/STF [semente]); prescrição quinquenal (Decreto n.º 20.910/1932,
  art. 1º; Súmula 85/STJ [semente]), distinguindo fundo de direito e trato sucessivo.
- **Militares estaduais**: Estatuto (Lei Estadual n.º 5.346/1992, com sete leis alteradoras
  listadas no SAPL [semente]); promoções (Lei Estadual n.º 6.514/2004, art. 23 e alteradoras
  [semente]) e **IRDR Tema 3/TJAL** [semente] (preterição, ônus, prescrição do fundo de direito em cinco
  anos, sem litisconsórcio necessário, sem promoção *per saltum*, sem efeitos financeiros
  retroativos); Conselho de Justificação (IAC Tema 2/TJAL [semente]).
- **Concurso público**: Temas 161, 784, 485 e 671/STF; SV 43 e 44 [semente].
- **Responsabilidade civil do Estado** (art. 37, § 6º, da CF): ação contra o Estado, não contra o
  agente (Tema 940/STF [semente]); morte de detento (Tema 592/STF [semente]); crime praticado por
  foragido (Tema 362/STF [semente]); prescrição quinquenal (Tema 553/STJ [semente]); dano moral pelo
  método bifásico adotado pela unidade.
- **Improbidade**: Lei n.º 8.429/1992 com a Lei n.º 14.230/2021; Tema 1.199/STF [semente] [conferir as
  ADIs sobre a Lei n.º 14.230/2021 e a prescrição].
- **Mandado de segurança**: Lei n.º 12.016/2009, arts. 7º, 14, 23 e 25 [semente]; ADI 4.296 [semente];
  encampação (Súmula 628/STJ [semente]).
- **Tributos estaduais** (ICMS, IPVA, ITCMD, taxas): depósito integral e em dinheiro (Súmula 112/STJ
  [semente]); TUST e TUSD na base do ICMS (Tema 986/STJ [semente]); DIFAL (Tema 1.093/STF [semente]);
  repetição e consectários (item 3); legislação tributária estadual no SAPL [conferir].
- **Licitações, contratos e previdência estadual**: leis federais e estaduais conferidas no caso
  [conferir].

## 5. Cumprimento de sentença contra o Estado

- Arts. 534 e 535 do CPC [semente]: demonstrativo discriminado; impugnação em 30 dias (prazo próprio,
  sem dobro); excesso com o valor que o executado entende correto; inexigibilidade por decisão do STF.
- **Requisitório**: RPV do Estado de Alagoas até o **maior benefício do RGPS** por beneficiário (Lei
  Estadual n.º 7.154/2010, art. 1º [semente]); pagamento da RPV em dois meses (art. 535, § 3º, II, do
  CPC, declarado constitucional na ADI 5.534 [semente]), a confrontar com os 90 dias do art. 2º da Lei
  n.º 7.154/2010; regime do valor incontroverso pelo total da condenação (ADI 5.534 e Tema 28/STF
  [conferir]). Precatório: art. 100 da CF [semente], com os limites anuais do § 23 (EC 136/2025) para
  o pagamento, sem efeito sobre o que se decide. Juros no prazo constitucional: SV 17 [semente],
  confrontada com o art. 97, § 16, do ADCT [conferir a conciliação].
- **Honorários**: devidos no cumprimento individual de sentença coletiva, ainda que não impugnado
  (Súmula 345/STJ e Tema 973/STJ [semente]); no mais, art. 85, § 7º.
- **Sequestro**: de precatório, só pelo Presidente do Tribunal (art. 100, §§ 6º e 27, da CF); a vara
  não o determina. Na RPV vencida, observe o art. 535, § 3º, II, e a jurisprudência conferida.

## 6. Comandos, intervenção do Ministério Público e última linha

- Fecho nos feitos da Fazenda (padrão dos modelos da 17ª Vara, `redacao.md`, item 5): último parágrafo
  **"P. R. I."** (sentença) ou **"Cumpra-se."** (decisão e despacho); a intimação pessoal da Fazenda
  Pública (art. 183, § 1º, do CPC) vai num dos comandos de cumprimento, no imperativo impessoal
  ("Intime-se o Estado de Alagoas pessoalmente…"). A linha "Publicações via DJEN…" não se usa nesta unidade.
- Ministério Público: mandado de segurança (art. 12 da Lei n.º 12.016/2009), ação civil pública,
  improbidade, interesse de incapaz (art. 178, II, do CPC) [conferir cada hipótese no caso].

## 7. Armadilhas próprias

- Aplicar a Selic da EC 113/2021 depois da EC 136/2025 sem pesquisa (Tema 1.419 e seus embargos); ou
  aplicar o IPCA mais 2% do art. 97, § 16, do ADCT à fase de conhecimento (é regra de requisitório).
- Decidir medicamento não incorporado sem examinar o ato de não incorporação e a negativa (Tema
  1.234, item IV); ignorar o marco de 19/09/2024 da competência federal.
- Remessa necessária com o limite errado (para o Estado é 500 salários mínimos) ou esquecida.
- Honorários por equidade fora do § 8º; negar honorários à Defensoria com base na Súmula 421/STJ.
- Condenar o Estado em custas (é isento), esquecendo, porém, o reembolso das despesas antecipadas.
- Declinar ao Juizado matéria excluída (saúde, concurso, promoção, tributo, previdência) ou manter na
  vara causa do Juizado; ignorar a competência da 28ª Vara quando o autor for criança ou adolescente.
- Ignorar IRDR e IAC do TJAL (militares, licença-prêmio) ou decidir processo alcançado por
  suspensão nacional.
- Contar prazo da Fazenda pelo DJEN; conceder dobro em prazo próprio; mandar a vara sequestrar
  verba de precatório.
