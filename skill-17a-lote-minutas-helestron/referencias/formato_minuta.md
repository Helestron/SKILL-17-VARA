# Marcação, portão e geração do Word

A minuta é redigida num `.txt` UTF-8 (`<pasta do processo>/minuta.txt`, caminho dado por
`autos.py caminhos N`) e convertida em `.docx` por `scripts/gerar_minuta.py`. **Os parágrafos não
são numerados**: o usuário aplica a numeração no editor do SAJ, no lançamento manual.

## 1. Marcação

Uma linha por parágrafo (linha em branco não conta):

| Linha | Vira |
|---|---|
| `@ato sentença` / `@ato decisão` / `@ato despacho` | diretiva obrigatória (1ª linha útil) |
| `@processo 0714346-41.2024.8.02.0001` | nome do arquivo e cabeçalho da anotada |
| texto | parágrafo do corpo: Times 12, recuo 2,5 cm, 1,5, justificado |
| `> texto` | transcrição em bloco: Courier New 10, recuo 4 cm, simples |
| `!! texto` | parágrafo decisório: negrito e sublinhado inteiros (conclusão de preliminar, prejudicial ou incidente; tese central do mérito) |
| `__ texto` | parágrafo inteiro sublinhado (comando que não abre por verbo de comando) |
| `%% texto` | nota só da anotada, em vermelho |
| `// texto` | comentário, ignorado |

Automático: "É o Relatório." em negrito; o parágrafo que abre por "Diante do exposto" ou "Do exposto"
em negrito e sublinhado (não marque `**` nele); depois do dispositivo, o parágrafo que abre por
verbo de comando ("Intime-se", "Expeça-se", "Retire-se", "Após,", "Em seguida,", "Serve a
presente", "À SPU,"…) sublinhado; itálico nos termos de `scripts/termos_italico.txt` (amplie a
lista quando preciso).

Em linha: `**negrito**`, `__sublinhado__`, `*itálico*`, `{{apontamento vermelho}}` (só na anotada),
`{{! dado vermelho que fica na limpa}}` (só o parêntese de Sisbajud/Renajud), `\*` para asterisco
literal.

Exemplo (sentença, trecho):

```
@ato sentença
@processo 0714346-41.2024.8.02.0001
Trata-se de Ação Ordinária proposta por **Fulano de Tal**, qualificado, em face do **Estado de Alagoas**.
O autor, militar da ativa, ocupa a graduação de 2º Sargento e busca a promoção por ressarcimento de preterição à graduação de 1º Sargento (fls. 1/12).
O Estado de Alagoas contestou às fls. 50/61. Arguiu a coisa julgada e, no mérito, sustentou a falta dos requisitos do art. 20 da Lei Estadual n.º 6.514/2004.
Réplica às fls. 70/75.
É o Relatório.
No que concerne à **coisa julgada**, a ação anterior buscou a promoção a contar de 2020, ao passo que esta se funda em preterição ocorrida em 2023 (fls. 55/58).
!! Desse modo, afasto a prejudicial de coisa julgada.
No mérito, o Tribunal de Justiça de Alagoas fixou, no IRDR n.º 3, a seguinte tese:
> 1.1. O mero cumprimento do interstício temporal no posto não implica preterição e, por essa razão, não gera direito automático à promoção.
Com efeito, o autor não comprovou o curso exigido pelo art. 20, VI, da mesma lei (art. 373, I, do CPC). {{Conferir: certificado às fls. 30, ilegível}}
Diante do exposto, julgo improcedente a demanda.
Condeno a parte autora nas custas e em honorários de R$ 1.000,00 (um mil reais), nos termos do art. 85, § 8º, do CPC, __com a exigibilidade suspensa (art. 98, § 3º, do CPC)__.
Com o trânsito em julgado, **arquivem-se os autos com a devida baixa**, independentemente de nova determinação.
P. R. I.
```

Campo cujo dado não está nos autos: `[ ]` com `{{Conferir: …}}`. Dúvida jurídica relevante e
insuperável: a minuta segue a solução principal, e a alternativa vai em nota logo abaixo do
parágrafo (`%% ALTERNATIVA — <texto alternativo e razão>`), só na anotada — o magistrado escolhe.

## 2. Portão

```
python -I scripts/verificar_minuta.py <minuta.txt>
```

JSON com `OK` ou `BLOQUEADO`, `pendencias_bloqueantes` e `apontamentos`.

- **Bloqueiam**: diretiva `@ato` ausente; **numeração manual de parágrafo**; título ou epígrafe
  interna; parágrafo inteiro em negrito no corpo; vocabulário vedado (`redacao.md`, item 8);
  linguagem de método; primeira pessoa fora do dispositivo e dos parágrafos decisórios (`!!`);
  sigla pronunciada como palavra em caixa alta; citação de mais de ~55 palavras entre aspas;
  "À SPU:"; perícia sem perito nomeado; marcação desbalanceada; parágrafo de mais de 170 palavras;
  na sentença, a falta de "Trata-se de" com partes em negrito, de "É o Relatório.", de "Diante do
  exposto, julgo", do parágrafo de arquivamento ou de "P. R. I." no fim; na decisão e no despacho,
  a falta de "Cumpra-se." no fim.
- **Apontamentos** (reexamine um a um; o que ficar, justifique com `autos.py marcar … --justificativa`):
  gerúndio, travessão, dois-pontos fora da introdução de transcrição, parágrafo acima de 110
  palavras, palavra repetida quatro vezes, frase curta e solta, abertura que nega o direito em frase
  curta, data no relatório, tema não aplicado, comando de certificação, "posto que", "§8º", "nº",
  sigla minúscula, caixa alta desconhecida, ideia repetida, precedentes em série, transcrição
  excessiva, extensão acima da referência, honorários ou remessa necessária não consignados.

O verificador é rede de segurança, **não substitui** a leitura crítica nem a revisão adversarial.

## 3. Geração

```
python -I scripts/gerar_minuta.py <minuta.txt> --saida "<pasta das minutas do lote>"
```

Roda o portão e, com `OK`, grava `Minuta_<processo>_<ato>_anotada.docx` (vermelhos, notas e a
ressalva de apoio, para revisão do magistrado) e `Minuta_<processo>_<ato>.docx` (limpa, para copiar
no editor do SAJ), e confere o XML de ambas (nenhum vermelho de apontamento, nota ou marca na limpa;
nenhuma numeração automática; dispositivo em negrito e sublinhado; transcrições em Courier). Com
`BLOQUEADO`, não grava nada; `--rascunho` grava só a anotada, com as pendências no topo, para
exame. **Gere sempre de novo a partir do .txt vigente** depois de qualquer correção.

## 4. Modelos

`python -I scripts/importar_modelo.py buscar "<classe> <tema> <desfecho>"` ordena os modelos da
skill e os de `pastas.modelos_usuario`; `importar_modelo.py <arquivo .docx|.rtf|.odt>` converte um
modelo para esta marcação (negrito, sublinhado, itálico, transcrições e parágrafos decisórios
preservados; cabeçalho e assinatura como comentário).
