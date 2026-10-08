# Banco de peritos — regras de nomeação

Fonte: lista oficial do banco de peritos do TJAL (PDF exportado do sistema, 16 páginas), texto
integral pesquisável em `referencias/peritos_banco_integral.txt` (colunas: Nome | E-mail | Área
de Atuação | Tipo). Um mesmo perito aparece em várias linhas, uma por área cadastrada. O banco é
estadual: antes de nomear, confira se o perito atua na comarca da unidade (o próprio cadastro ou
uma nomeação anterior do juízo) — perito de outra região eleva custo e prazo da perícia.

## Regras de escolha

1. **A nomeação sai pronta na própria minuta** que defere ou determina a perícia — com nome,
   especialidade e e-mail do banco (e telefone, quando constar). **Nunca** determinar que a
   secretaria certifique, localize ou escolha perito: a escolha é ato do juízo.
2. **Especialidade define-se pelo objeto da prova**, não pelo rótulo genérico: assinatura
   contestada → grafotécnica; assinatura digital/eletrônica, integridade ou adulteração de
   documento eletrônico, protocolo de assinatura → documentoscopia/autenticidade documental;
   impressão digital → papiloscopia; débito bancário, juros, encargos → perito contábil; imóvel
   (valor, vício construtivo, confrontação) → avaliador de imóveis/engenheiro civil (ou agrimensor,
   em demarcatória); incapacidade laboral → médico do trabalho ou especialidade clínica
   pertinente (ortopedia, neurologia, psiquiatria); interdição/curatela → psiquiatra, com estudo
   psicossocial por psicólogo/assistente social; veículos e acidentes → engenheiro mecânico/perito
   em acidentes de trânsito; DNA → laboratório habilitado (ou o convênio do tribunal, se houver).
3. **Rodízio**: alterne as nomeações entre os peritos do banco cadastrados na área exigida,
   **priorizando os usualmente nomeados pelo juízo** (seção "Usuais do juízo" abaixo, construída a
   partir das nomeações da própria unidade). Não repita o mesmo perito em dois processos do mesmo
   lote se houver alternativa usual na mesma especialidade; anote cada nomeação na lista de
   trabalho para controlar o rodízio do lote.
4. **Impedimento e suspeição** (arts. 148, II, e 144–145 do CPC): antes de nomear, confira a
   autoria das peças técnicas e médicas dos autos — o médico assistente da parte, o contador que
   elaborou o cálculo, o engenheiro que assinou o laudo particular **não podem** ser o perito do
   juízo. Registre a verificação no plano de análise.
5. **Honorários e adiantamento**: quem requer a perícia adianta os honorários (art. 95 do CPC);
   determinada de ofício ou requerida por ambas as partes, rateia-se. Beneficiário da gratuidade:
   observar a Resolução TJAL n.º 12/2012 (pagamento após o laudo, pelo tribunal) — indefira o
   adiantamento e consigne a forma de pagamento. Fixe na mesma decisão o prazo para o laudo, a
   intimação do perito para proposta de honorários e o prazo das partes para quesitos e
   assistentes técnicos (art. 465, § 1º, do CPC).
6. **Prova pericial desnecessária, impertinente ou impossível** é indeferida na própria decisão
   (arts. 370, parágrafo único, 464, § 1º, e 443 do CPC), com o motivo — a nomeação só ocorre
   quando a perícia é útil ao julgamento.

## Como consultar o banco na execução

Busque a especialidade no arquivo integral e colete os nomes cadastrados:

```
grep -i -B3 "<especialidade>" referencias/peritos_banco_integral.txt
```

(termos úteis: Grafotécnica, Papiloscop, Documentoscopia, "Perito contábil", contador,
"Avaliador de im", "Engenheiro civil", Ortopedista, Psiquiatra, Psicólog, "Assistente social",
"Médico do trabalho", Neurolog, Cardiolog, Agrimens, "Engenheiro mecânico"). O nome pode estar na
linha anterior à área (layout de coluna quebrada) — confirme nome + e-mail + área antes de
nomear.

## Usuais do juízo (rodízio — atualizar a cada nomeação)

Seção inicialmente vazia para esta unidade. **Acrescente aqui cada perito nomeado em minuta**
(nome, e-mail, especialidade, processo e data) e também os peritos que os atos recentes do próprio
juízo, lidos nos autos, mostrem como habituais — o rodízio passa a priorizá-los. Ao entregar o
lote, proponha a atualização deste arquivo no pacote revisado da skill (item "Autodesenvolvimento"
do SKILL.md), sem alteração silenciosa.

- (nenhuma nomeação registrada até a criação da skill, em 25/09/2026)
