# Fase 2 — Pesquisa e verificação de precedentes, suspensões e normas

Redigir de memória e conferir depois obriga a reescrever fundamentações inteiras. Por isso, entre a
leitura e a redação, levanta-se e confere-se **tudo** o que a minuta vai citar. **Só se cita o que
tem entrada `VERIFIED` no ledger** (`scripts/ledger.py`); o que não se confirmar não se cita.

## 1. O que se pesquisa em cada processo

1. **Teses de que a solução depende**, a partir da classe, do assunto, do pedido e das defesas.
   Leia antes o módulo de competência pertinente (`fazenda_publica_estadual.md`,
   `execucao_fiscal.md`): ele indica temas, suspensões, consectários e normas a conferir — orienta a
   pesquisa, **não autoriza citar**.
2. **Adequação a temas repetitivos do STJ, repercussão geral do STF e IRDR/IAC do TJAL** — análise
   obrigatória em todo processo, com a conclusão no ledger (incide ou não, e por quê). Na minuta o
   tema só aparece quando aplicado ou invocado por uma parte.
3. **Suspensão nacional** (art. 1.037, II, do CPC) em toda matéria de massa: distinga a suspensão
   restrita a REsp/AREsp (não alcança o primeiro grau) da de todos os processos (alcança). Confronte o
   **objeto real** da demanda com a afetação. Decidir feito suspenso é risco de nulidade.
4. **Normas** citadas, na redação vigente (Planalto; SAPL da Assembleia de Alagoas para lei
   estadual): leis recentes alteram dispositivos que a memória dá por estáveis.
5. **Doutrina**: só com autor, obra, edição, editora, ano e página conferidos na fonte; sem página
   conferida, não se cita. Os modelos da vara fundamentam sobretudo em lei e precedente — a doutrina
   entra quando acrescenta, nunca como ornamento.

## 2. Hierarquia de fontes

- **Primárias** (autorizam a citação): STF (pesquisa de jurisprudência, repercussão geral, súmulas);
  STJ (base de acórdãos, **Portal de Dados Abertos**, Informativos, Jurisprudência em Teses,
  súmulas); TJAL (jurisprudência de 2º grau, IRDR e IAC — orientação das Câmaras Cíveis, filtro
  recursal imediato, sem jamais prevalecer sobre o STJ); Planalto e SAPL (lei).
- **Comprovação de autenticidade**: o JusBrasil (sessão do usuário no navegador) vale para conferir
  o inteiro teor ou a ementa oficial de precedente do STJ e do STF, com `origem: "jusbrasil"` no
  ledger.
- **Pista, nunca citação**: JusIA e qualquer assistente generativo (ementa parafraseada, número
  trocado e precedente inexistente com frequência conhecida), blogs, sítios de escritórios, e o
  precedente que os próprios modelos da vara tragam sem conferência.
- **Prevalência do STJ**: divergindo o entendimento da unidade (inclusive o dos modelos) da
  jurisprudência do STJ, prevalece o STJ, com a divergência em vermelho na anotada. Se ambos levam ao
  mesmo resultado por caminhos diversos, enfrente os dois.

## 3. Rotas de acesso, nesta ordem

1. **Cache do ledger**: `ledger.py buscar <termos> -t <T>` — entrada `VERIFIED` com menos de 30 dias
   se reaproveita sem nova pesquisa.
2. **STJ — Portal de Dados Abertos** (via oficial para consulta automatizada, sem CAPTCHA):

   ```
   python -I scripts/stj_dados_abertos.py conjuntos --filtro espelhos -t <T>
   python -I scripts/stj_dados_abertos.py baixar --conjunto <id> --desde 202301 -t <T>
   python -I scripts/stj_dados_abertos.py buscar "promoção militar interstício" --classe REsp -t <T>
   python -I scripts/stj_dados_abertos.py tema 1076 -t <T>
   ```

   Os "espelhos de acórdãos" de cada órgão julgador (Primeira e Segunda Seções e Turmas para direito
   público; Corte Especial) baixam-se uma vez por mês de interesse e ficam no cache. O resultado já
   vem no formato do ledger, com `status: "PENDENTE"`: leia a ementa, confira a aderência ao caso,
   ponha `VERIFIED`, preencha `aderencia` e grave (`ledger.py add`).
3. **Página oficial por WebFetch** (STF, STJ, TJAL, Planalto, SAPL), com pedido de transcrição
   literal; pontos de partida em `config/vara.json > jurisprudencia_rotas`.
4. **Navegador do usuário** (Claude in Chrome ou o navegador do aplicativo), na sessão dele — rota
   para páginas que recusam acesso automatizado e para o JusBrasil (item 4).
5. **Rota oficial alternativa** do mesmo órgão: inteiro teor em PDF, portal de súmulas, notícia
   oficial do julgamento com o número do processo (para achar o acórdão, não para citar).
6. Nada disso confirmou → **não se cita**. A fundamentação se apoia no que foi conferido (lei,
   precedente vinculante já no ledger), e a lacuna vai em vermelho na anotada se for relevante.

## 4. Desafios de verificação (CAPTCHA, Cloudflare e afins) — o usuário resolve

Alguns portais (o SCON do STJ, entre eles) exibem, de tempos em tempos, uma verificação anti-robô:
caixa "Não sou um robô", desafio de imagens, tela "Verificando se você é humano". **A skill não
resolve, não marca, não contorna nem automatiza esses desafios** — nem por clique programado, nem por
serviço de resolução, nem por navegador disfarçado, nem pela reutilização de cookies de liberação
fora do navegador do usuário. Esses mecanismos existem justamente para barrar a automação; contorná-los
viola as condições de uso dos portais e pode levar ao bloqueio do endereço de rede do tribunal,
o que prejudicaria todos os usuários do TJAL.

O fluxo que mantém a execução praticamente desassistida:

1. A via principal para o STJ é o Portal de Dados Abertos (item 3.2), que não tem desafio.
2. Aparecendo o desafio no navegador do usuário, a skill **para essa consulta**, avisa **uma vez**,
   em uma linha ("Resolva a verificação aberta na aba do STJ; sigo sozinho em seguida.") — o gancho de
   aviso (`scripts/avisar.ps1`, configurado por `executar_lote.ps1`) toca e mostra um balão no
   Windows —, e **segue com os demais processos e consultas** enquanto espera.
3. Resolvido pelo usuário, a sessão do navegador dele continua liberada por um tempo, e as consultas
   seguintes passam sem nova interrupção.
4. Na execução sem janela (`executar_lote.ps1 -SemInteracao`), não há quem resolva: a consulta segue
   pelas rotas 1, 2, 3 e 5, e o que só o portal protegido confirmaria fica sem citação e registrado
   na lista de trabalho.

O mesmo vale para login, assinatura ou conteúdo de assinante: autenticação é ato do usuário. Nunca
digite nem armazene senha, PIN, token ou código.

## 5. Delegação a subagentes e ledger

- Agrupe as consultas por tema e delegue a subagentes, em paralelo. Cada um devolve, por citação
  candidata: número do recurso, órgão julgador, relator, datas de julgamento e publicação, fonte
  (URL), **transcrição literal** do trecho pertinente e a aderência aos fatos do caso — já no
  formato do ledger (`ledger.py`, docstring), com `VERIFIED` ou `REJECTED`.
- O subagente recebe a questão jurídica **em abstrato** (nunca nome de parte nem dado de processo
  sigiloso) e a regra deste arquivo: fonte oficial, transcrição literal, nada de memória.
- Grave com `ledger.py add <arquivo.json> -t <T>`; a gravação recusa campo obrigatório ausente e
  fonte não oficial.
- Antes da revisão adversarial, `ledger.py conferir <minuta.txt> -t <T> --calculos <calculos.json>`:
  precedente, súmula ou tema citado sem entrada `VERIFIED` bloqueia; valor em reais sem lastro no
  ledger de cálculos é apontamento.

## 6. Cálculos

Nenhuma conta entra na minuta "de cabeça": `ledger.py calc <calculos.json> entrada --descricao …
--valor … --fls …` para o valor colhido dos autos e `ledger.py calc <calculos.json> add --descricao …
--expr "…"` para cada operação. Refaça toda conta das partes; aponte nominalmente acertos e erros;
jamais estime índice que não possa obter com segurança — fixe os critérios e remeta a apuração à
Contadoria; no cumprimento de sentença, o título governa (interpreta-se o obscuro; não se substitui
o claro).
