# Código de Normas da CGJ/AL — digesto orientador para despachos e comandos

Fonte: Provimento n.º 13, de 24/05/2023 (Código de Normas da Corregedoria-Geral da Justiça de
Alagoas), texto consolidado com as alterações até o Provimento de 2024 listadas no preâmbulo.
Texto integral pesquisável em `referencias/cgj_normas_integral.txt` (busque por "Art. NNN").
Uso: orientar (i) o que NÃO se determina à secretaria por já ser dever de ofício dela; (ii) a
forma dos comandos que efetivamente precisam de ordem judicial; (iii) obrigações de cumprimento
das partes. Citar artigos do Código nas minutas apenas conferindo-os no texto integral.

O Código vale para todas as unidades do primeiro grau do TJAL. O que muda de unidade para
unidade é **quem cumpre**: nas unidades atendidas pela Secretaria de Processamento Unificado, os
comandos dirigem-se à **SPU**; nas demais, à **Secretaria** da própria unidade. A skill trata
isso como parâmetro (`redacao.abertura_comando` em `config/vara.json`; vazio = imperativo impessoal, como nos modelos; confirmado pela leitura dos
atos recentes do próprio juízo nos autos).

## 1. O que a serventia faz DE OFÍCIO — nunca comande o que o Código já manda (arts. 383–388)

**Art. 383**: ato ordinatório é o instrumento pelo qual o servidor impulsiona o feito quando
isso não depende de ato do juiz. **Art. 384**: sempre que o andamento depender de ato de mero
expediente, sem conteúdo decisório, o servidor DEVE valer-se de ato ordinatório,
**independentemente de despacho**, especialmente:

- **Inicial (§ 1º)**: intimar o autor para esclarecer divergência de qualificação (5 dias);
  retificar dados das partes; intimar para recolher custas (inclusive remanescentes); juntar
  procuração/substabelecimento e atualizar endereços.
- **Citação/intimação frustrada (§ 2º)**: expedir mandado ou precatória quando a carta postal
  voltar "recusado/ausente/não atendido"; intimar o autor (15 dias) quando voltar
  "mudou-se/desconhecido/endereço inexistente/insuficiente"; reiterar citação/intimação por
  carta quando indicado novo endereço; devolvido mandado/precatória sem cumprimento, vista de
  5 dias a quem requereu.
- **Resposta do réu (§ 3º)**: apresentada contestação com preliminares ou documentos, intimar o
  autor para réplica em 15 dias; havendo reconvenção, intimar o reconvindo para contestar.
- **Instrução e impulso (§ 4º)**: intimar a parte contrária sobre documentos novos (5 dias);
  intimar sobre proposta de honorários periciais e sobre o laudo (15 dias); intimar para
  apresentar cálculo ou manifestar-se sobre o da outra parte (5 dias); intimar sobre respostas
  a ofícios de diligências (5 dias); cobrar laudo vencido do perito (24h); intimar testemunhas
  tempestivamente arroladas (correio, ou mandado se inviável/AR negativo); expedir precatória
  para oitiva de residente fora da comarca; expedir guias de depósito requeridas; intimar para
  dados bancários (5 dias); intimar o interessado a dar prosseguimento após decorrida a
  suspensão (5 dias); desarquivar; certificar, na tutela cautelar antecedente, o decurso dos 30
  dias e a dedução (ou não) do pedido principal, fazendo conclusão.
- **Renúncia de mandato (§ 5º)**; **precatórias (§ 6º — ver também art. 386**: o cumprimento da
  missiva independe de despacho do juízo deprecado**)**.
- **Execução/cumprimento (§ 7º)**: vista ao exequente sobre nomeação de bens, depósito, penhora
  on-line e ausência de embargos; termos de penhora e depósito; intimações de penhora (cônjuge,
  terceiro garantidor), registro, avaliação e hastas; intimar o credor após hasta negativa
  (5 dias) e para adjudicação/alienação particular.
- **Recursos (§ 8º)**: contrarrazões de apelação (art. 1.010, §§ 2º e 3º, CPC) e de embargos de
  declaração (5 dias); remessa ao órgão recursal; ciência do retorno da instância superior COM
  cumprimento imediato do acórdão/sentença; cálculo e cobrança de custas finais.
- **Trânsito em julgado (§ 9º)**: **expedir todos os documentos e cumprir todas as
  determinações constantes da sentença**; arquivar após comunicações, anotações, inscrições,
  registros e cobranças.

**Art. 385**: os prazos do art. 384 valem apenas à falta de prazo legal diverso. **Art. 387**:
prazo residual de 5 dias para as providências. **Art. 388**: todo ato ordinatório é revisível
de ofício ou a requerimento.

**Consequência para as minutas**: comandar à secretaria providência do art. 384 é redundante —
o Código já a impõe. Comande apenas o que exige ordem judicial (atos com conteúdo decisório,
diligências fora do rol, expedições que dependem de deliberação: ofícios a órgãos, alvarás,
editais com particularidades, bloqueios, mandados de averbação etc.).

## 2. Certidões (arts. 331–335) — a serventia certifica o que consta; o gabinete lê o que consta

**Art. 331**: certidão comprova ato ou assentamento constante de processo, livro ou documento
da unidade, ou fato havido em suas dependências. **Art. 332**: havendo requerimento, o servidor
certifica **independentemente de despacho** qualquer ato do processo (5 dias). **Art. 334**:
certidão de comparecimento em 2 dias úteis (modelo cat. 13, cód. 1812). **Art. 334, parágrafo
único**: certidões fora desses limites dependem de decisão do juiz.

**Consequência**: jamais determinar "certifique-se" sobre evento, manifestação ou prova **já
registrados nos autos** — o gabinete verifica por leitura direta e afirma na fundamentação com
as fls. Determina-se certificação apenas de evento **externo/não inserido** no processo,
derivado de despacho anterior que atribuiu tarefa ainda não certificada (ex.: resposta de
ofício não juntada, publicação de edital não comprovada, devolução de precatória).

## 3. Expedição de documentos (arts. 316–319 e Seções do Cap. VI)

**Art. 316**: mandados, certidões, alvarás, autos, cartas (precatórias/rogatórias/de ordem),
ofícios, termos, editais, atos ordinatórios, formais, despachos, decisões e sentenças
expedem-se **exclusivamente pelo Sistema SAJ, pelo fluxo do processo** (nas unidades já
migradas, pelo e-Proc). **Art. 317**: vedado usar modelo diverso do específico determinado pelo
Código; vedada criação/modificação de modelos sem autorização do Corregedor. **Art. 317-A**:
correspondência com AR usa modelo "AR DIGITAL". **Art. 318**: qualquer servidor
efetivo/comissionado/cedido pode expedir e assinar documentos, salvo exigência legal de cargo.
**Art. 319**: conteúdo publicável vai na ferramenta "Complemento da Movimentação", selecionado
apenas o trecho pertinente (no lançamento manual da minuta no SAJ, feito pelo usuário).

**Alvarás (arts. 336–341-B)**: alvará consubstancia autorização do juiz; redação sem margem a
dúvida quanto a objeto e limites; levantamento preferencialmente eletrônico; novo alvará exige
tornar sem efeito o anterior; observações restringindo liberação ao beneficiário indicado
(341-A); em obrigação personalíssima (tratamento/medicamento), a decisão e o alvará consignam o
dever de abstenção em caso de mudança da situação, comunicável em 10 dias úteis (341-B).

**Autos (arts. 342–345)**: registram acontecimentos externos ou com repercussão material
(arrematação, adjudicação, constatação, entrega, depósito).

## 4. Audiências (arts. 404–409, 619)

**Art. 404**: **a designação de audiências é atribuição do juiz, delegável por portaria aos
servidores com critérios objetivos de pauta**; havendo delegação, pauta em 30 dias. A skill
trabalha com o parâmetro `redacao.designacao_audiencia` (`config/vara.json`): quando a unidade franqueia a designação à
Secretaria (praxe comum), o dispositivo diz "à Secretaria da Vara para designação de audiência
de instrução conforme a disponibilidade de pauta", sem fixar data; quando o próprio gabinete
pauta, a data fica entre colchetes para preenchimento. **Art. 405**: o servidor examina os
processos ao menos 5 dias antes da audiência para conferir intimações/requisições. **Art.
619**: na ata da audiência do art. 334 do CPC constam apenas presenças/ausências e questões do
acordo.

## 5. Intimações e comunicações

**Art. 263**: intimação de serventias extrajudiciais via portal, por ato ordinatório cód. 2057,
independentemente de despacho. **Art. 268**: comunicações a órgãos públicos via portal dirigem-se
ao órgão, não a agente individual. Publicações e intimações das minutas: via DJEN (o fecho da
minuta é "P. R. I." ou "Cumpra-se.", padrão da 17ª Vara), ressalvadas as intimações pessoais exigidas por lei (Ministério Público, Defensoria
Pública, Fazenda Pública e, no processo penal, o acusado — ver os módulos de competência).

## 6. Certidões cíveis e criminais de distribuição (arts. 589–600)

Expedição em horário próprio pela serventia (art. 62-A c/c 589 ss.); certidões de falência,
recuperação e execução fiscal individualizadas a requerimento (art. 600).

## Regras de uso deste digesto

1. Antes de redigir qualquer comando à secretaria, confronte-o com o art. 384: se a providência
   está no rol, **suprima o comando** — a serventia age de ofício; comandá-la é retrabalho.
2. Ao definir obrigação de cumprimento pelas partes (prazos de manifestação, juntada,
   recolhimento), prefira os prazos que o Código já assinala (5/15 dias, art. 384) salvo prazo
   legal ou judicial diverso — e lembre o prazo de 45 dias fixado pela skill para bancos e
   instituições financeiras apresentarem contratos e documentos.
3. Citação de artigo do Código na minuta: conferir antes o texto no arquivo integral
   (`grep "Art. NNN" referencias/cgj_normas_integral.txt`) — o digesto orienta, o integral
   autoriza.
