# Skill da 17ª Vara Cível da Capital — minutas a partir da pasta do Helestron

Skill para o Claude que elabora minutas de **sentença, decisão e despacho** da 17ª Vara Cível da
Capital (Fazenda Pública Estadual, Maceió/TJAL) a partir dos **autos em PDF já baixados pelo
aplicativo Helestron** e das **transcrições de audiências** do próprio aplicativo, e as entrega em
**Word (.docx)**, no padrão estilístico dos modelos da vara.

## Versão 2.1 (08/10/2026) — cumprimentos de sentença

- Módulo `referencias/cumprimento_sentenca.md`: fase do processo e ato de cada uma; requisitos do
  requerimento (art. 534 do CPC e Resolução TJAL n.º 21/2023); sucessão e habilitação (espólio,
  inventário, cônjuge sobrevivente, ônus de indicar endereço); cálculos, fichas financeiras e
  Contadoria; impugnação (art. 535); RPV, precatório e honorários; cessão de crédito; redação dos
  despachos no padrão da vara.
- Quatro modelos de despacho de cumprimento (`modelos/despacho_CS_*`, com os originais).
- Enumeração recuada (`+ i)`, `++ a)`) no Word, como no despacho de adequação; fecho "Cumpra-se
  observada a sequência acima.".
- `autos.py relacionados N` (autos de conhecimento e demais sequenciais, extraídos junto com o lote) e
  `autos.py requisitos N` (pistas, com as fls., de cada requisito e da fase).
- Portão com apontamentos próprios do cumprimento (custas, Contadoria, fichas financeiras, remissão a
  "item N").

## Versão 2.0 (08/10/2026) — o que mudou

| Pedido | Como ficou |
|---|---|
| 1. Sem a fase de download no e-SAJ | A Fase 1 lê a pasta de downloads do Helestron (`scripts/autos.py`, `scripts/ponte_helestron.py`); nada se baixa nem se acessa no e-SAJ |
| 2. Sem a inserção no SAJ | A tarefa termina na entrega de `Minuta_<processo>_<ato>.docx` (limpa) e `…_anotada.docx` (com os apontamentos em vermelho); removidos `saj_auto.ps1`, `fase3_saj_17a.md` e a saída RTF |
| 3. Modelos como padrão | `modelos/` (marcação + originais) e `referencias/estilo_modelos.md`: arquitetura do ato, relatório, perfil de análise, retórica, destaques, formatação medida nos modelos e vícios a não reproduzir |
| 4. Sem numeração de parágrafos | O gerador não numera e o portão bloqueia numeração manual |
| 5. Execução integral sem permissões | `scripts/instalar.ps1` (instala e cria o atalho), `scripts/executar_lote.ps1` (sessão em modo sem permissões, só para a skill), `scripts/avisar.ps1` (bipe e balão quando a sessão precisa do usuário). Pesquisa no STJ pelo **Portal de Dados Abertos** (`scripts/stj_dados_abertos.py`), via oficial sem CAPTCHA. Desafios de CAPTCHA ou Cloudflare **não são resolvidos automaticamente**: o usuário os resolve na janela dele (ver abaixo) |
| 6. Redação objetiva | Regras de enxugamento com exemplos tirados dos modelos; o portão aponta extensão, ideia repetida, precedentes em série e transcrição excessiva; a revisão adversarial confere a verborragia, sem perda de enfrentamento |
| 7. Integração com o Helestron | Localização automática do Python, da pasta de downloads, da de sigilosos e da de **transcrições de audiências** (txt, docx, srt, vtt, json), associadas a cada processo |

**Sobre CAPTCHA e Cloudflare.** A marcação automática de CAPTCHA e o contorno da verificação do
Cloudflare não foram implementados: esses mecanismos existem para barrar acesso automatizado, e
contorná-los viola as condições de uso do portal e pode levar ao bloqueio da rede do tribunal. Em
lugar disso, o STJ é consultado pelo seu Portal de Dados Abertos (feito para acesso automatizado), e,
quando uma página protegida for indispensável, a sessão avisa o usuário (som e balão no Windows),
espera que ele resolva o desafio no próprio navegador e segue com o restante do lote nesse meio-tempo.

## Instalação e uso (Windows)

1. Baixe `dist/skill-17a-lote-minutas-helestron.zip` e extraia.
2. PowerShell: `& '<pasta extraída>\skill-17a-lote-minutas-helestron\scripts\instalar.ps1' -Pasta '<downloads do Helestron>'`
3. Abra o atalho **Minutas 17a Vara** da Área de Trabalho (na primeira vez, aceite o aviso do modo
   sem permissões do Claude Code), ou rode `executar_lote.ps1 -Pasta … -Lista '…'`.

No claude.ai ou no Cowork, envie o `.zip` como skill e conecte a pasta de downloads do Helestron à
sessão. Detalhes em `skill-17a-lote-minutas-helestron/referencias/automacao.md`.

## Estrutura

```
skill-17a-lote-minutas-helestron/
  SKILL.md                 fluxo em quatro fases (autos → pesquisa → minuta → revisão e entrega)
  config/vara.json         unidade, pastas, formatação, fórmulas, fontes oficiais
  config/claude_execucao.json   gancho de aviso e lista de permissões do lançador
  modelos/                 modelos da vara em marcação; originais em modelos/originais/
  referencias/             estilo_modelos, redacao, formato_minuta, autos_helestron,
                           pesquisa_fontes, automacao + módulos de Fazenda Pública,
                           execução fiscal, Código de Normas da CGJ/AL e peritos
  scripts/                 Python (biblioteca padrão) e PowerShell
testes/                    testes de ponta a ponta (pasta sintética do Helestron)
empacotar.py               gera dist/skill-17a-lote-minutas-helestron.zip
```

## Testes

```
python3 testes/testar.py      # requer reportlab e pdfplumber ou pypdf (só para os testes)
python3 empacotar.py          # gera o .zip da skill
```

Os testes criam uma pasta que imita o acervo do Helestron (PDFs com marcadores, capa, sigiloso e
transcrições .srt e .json) e conferem inventário, lote, sigilo, leitura por folhas, transcrições,
portão (inclusive o bloqueio de parágrafo numerado), geração do Word (versão limpa sem vermelho e sem
numeração; formatação dos modelos), ledger de citações e de cálculos e a importação dos modelos.
O cliente do Portal de Dados Abertos do STJ foi testado com cache local; o acesso real ao portal
deve ser confirmado na primeira execução no computador do gabinete.
