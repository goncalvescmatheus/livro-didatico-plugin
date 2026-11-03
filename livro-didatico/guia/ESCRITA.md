# Guia de escrita: estilo e restrições

As regras R1 a R14 valem para todo texto que vai ao leitor: capítulos, apêndices, legendas, gabaritos, comentários de código mostrados no livro. Cada regra tem o motivo, um exemplo errado e um certo. O script `verificar_livro.py` encontra parte das violações automaticamente; as outras dependem de leitura.

---

## R1. Nenhum vazamento de pensamento ou de elaboração

O livro apresenta conhecimento, não a história de como foi escrito.

| Errado | Certo |
| --- | --- |
| "Corrigimos o fator de calibração, que antes estava em 0,19." | "Um fator de calibração de 0,19 está fora da faixa física; ele indica um erro de estrutura do modelo." |
| "Vou agora calcular o preço." / "Como discutimos na conversa…" | "O preço é…" / "Como mostra a seção 3.2…" |
| "Interpretação crítica do que fizemos." | "O que o exemplo ensina sobre os dados." |
| "(verificar)", "TODO", "a confirmar" no texto final | Fato verificado, com fonte; ou fora do livro |

Erros de um modelo aparecem como **lição sobre o método ou sobre os dados**, nunca como autocorreção.

## R2. Nenhuma referência a arquivos ou ferramentas internas do projeto

O leitor não tem acesso ao projeto. Não cite pastas, scripts, memória, plano, sessões ou ferramentas usadas para escrever.

| Errado | Certo |
| --- | --- |
| "A tabela é gerada por `codigo/apendices/gerar_glossario.py`." | (nada; a tabela simplesmente está ali) |
| "Os números vêm de `codigo/cap05/dcf.py`." | "O laboratório 5.6 constrói o modelo que produz estes números." |
| "Ver MEMORIA_DO_PROJETO." | (nada) |

Exceção: arquivos que **o leitor cria** seguindo o laboratório (`src/{{pacote}}/precos.py`, `config.yaml`) podem e devem ser nomeados.

## R3. Autocontido

- Todo termo é definido no livro, na primeira ocorrência; o glossário e a lista de siglas o repetem.
- Todo dado vem com o **código de acesso** (API, parâmetros, endpoint), nunca "os dados vieram de X".
- Pré-requisitos ficam no capítulo 0 e no Apêndice A.
- Referências externas servem para aprofundar, não para completar uma explicação que falta.

## R4. Construído com o leitor

- Fale com o leitor ("você" ou "nós" inclusivo), em voz ativa.
- Antes de resultados importantes, peça uma previsão ("Antes de continuar…").
- O caso condutor é montado pelo leitor; diga de que capítulo vem cada número reaproveitado.
- Diga o porquê de cada passo, não só o como.

## R5. Toda conta com todos os passos

Nenhum número aparece sem a operação que o produz, e nenhuma entrada sem origem.

1. **Origem de cada entrada.** Se a fonte dá uma faixa e o texto usa um valor, diga qual e por quê.
   - Errado: "O rendimento do equipamento cai $0{,}35\% \times 35{,}8 \approx 12{,}5\%$."
   - Certo: "O rendimento cai $\gamma\,(T - T_{\text{ref}}) = 0{,}35\% \times (60{,}8 - 25) = 0{,}35\% \times 35{,}8 \approx 12{,}5\%$, usando o meio da faixa de $\gamma$ (0,30% a 0,40% por °C) e a temperatura de referência do fabricante, 25 °C."
2. **Conversão de unidade ou de base é um passo próprio.**
   - Errado: "A receita sobe 12,5 € por central, ou seja, 125 € por sensor adicional."
   - Certo: "Passar de 1,4 para 1,5 sensores por central acrescenta $\Delta r = 0{,}1$ sensor por central; se a receita sobe 12,5 € por central, cada sensor adicional rende $12{,}5 / 0{,}1 = 125$ € por ano."
3. **Taxas marginais: derivada, forma equivalente e variação finita.** Ao apresentar $dE/dr$, mostre a derivada termo a termo, uma forma que torne explícito o que se desconta ($\sum_t x_t - \sum_t x_t\mathbf 1\{r x_t \ge 1\}$), a versão para um aumento finito ($\sum_t \min(\Delta r\,x_t, (1 - r x_t)^+)$) e um exemplo numérico em que as duas diferem.
4. **Resultado com unidade e em negrito** no fim de cada passo importante.
5. **Arredondamento só no fim**, com o mesmo número de casas do resto do capítulo.

## R6. Não misturar números

- **Uma base por cálculo:** não some € por central com € por sensor, potência com energia (kW com kWh), valor nominal com real, mensal com anual, sem converter explicitamente.
- **Um cenário por cálculo:** não use o preço de um cenário com o volume de outro.
- **Separadores do idioma** no texto, nas tabelas e nos eixos das figuras (português: `1.234,5`, sinal de menos "−"); ponto decimal só dentro de código.
- **Mesmo número em todo lugar:** texto, tabela, figura e gabarito mostram o mesmo valor com o mesmo arredondamento.
- **Faixas com unidade nos dois lados** quando houver risco de ambiguidade ("250 €/unidade a 350 €/unidade", ou "250 a 350 €/unidade" se a unidade é clara).

## R7. Siglas com parcimônia

Siglas repetitivas e abstratas tornam o texto ilegível.

- Escreva por extenso. Use sigla só se ela for **padrão da área** e aparecer **muitas vezes**.
- **Nunca crie siglas** para conceitos, cenários ou métodos do próprio livro ("o CR-B2 do caso PC-3").
- Expanda na **primeira ocorrência de cada capítulo**: "taxa interna de retorno (TIR, *internal rate of return*)".
- No máximo três siglas distintas por parágrafo; se passar disso, reescreva.
- Toda sigla usada está em `0s-siglas.md`, agrupada por área.

## R8. Tabelas limpas

- **Uma informação por coluna**, com a unidade no cabeçalho (`Receita (€/ano)`), e não em cada célula.
- **Células curtas.** Nada de parágrafos dentro da tabela; explicações vão no texto.
- **Não misturar número e texto na mesma coluna** (use "—" para ausente, e explique no texto).
- **Texto antes** (o que a tabela mostra e de onde vêm os dados) e **texto depois** (o que se conclui).
- **Tabelas de conteúdo e tabelas de referência separadas:** uma tabela compara números; outra lista definições. Não junte as duas.
- Linhas em ordem com sentido (crescente, cronológica, por importância), dita no texto.

## R9. Fórmulas

- Inline `$...$` **sem espaço** junto aos cifrões; destacadas `$$ … $$` em linhas próprias.
- Vírgula decimal dentro da fórmula como `{,}`: `$0{,}55$`.
- Acentos em subscritos com `\text{}`: `p_{\text{diário}}`.
- Operadores com `\operatorname{}` e conjuntos com `\mathbb{}`.
- Toda fórmula nova seguida de **Lendo a fórmula** (ver `PEDAGOGIA.md`, seção 6).
- Moedas com cifrão escapado no Markdown: `US\$`, `R\$`.

## R10. Código mostrado no livro

- Todo bloco com linguagem anotada (`python`, `bash`, `yaml`, `text`).
- Seguido de **Lendo o código**: o que cada parte faz em linguagem do domínio, de onde vêm os dados (cada parâmetro da API), as escolhas não óbvias.
- Comentários dentro do código também são texto do livro: sem vazamento (R1) nem referência interna (R2).
- Segredos (tokens) em variáveis de ambiente, nunca no código.

## R11. Estilo

- Frases curtas, voz ativa, um parágrafo por ideia.
- Números concretos em vez de adjetivos: "cai 37%", e não "cai muito".
- O mesmo termo para a mesma coisa em todo o livro. Termos técnicos com equivalentes em outras línguas na primeira ocorrência, se a ficha pedir.
- Negrito para resultados e termos definidos; itálico para termos estrangeiros.
- Hipóteses explícitas, com faixa e fonte ("hipótese de trabalho: 8% ao ano, faixa de 6% a 10%, fonte…").

## R12. Fatos e fontes

- Toda regra, data, valor de mercado e caso histórico é conferido em **fonte primária** (norma, regulador, operador, artigo original, base oficial). Leia o texto original, não só resumos.
- Fontes no fim de cada capítulo, com data de acesso quando forem páginas vivas.
- Dados com licença restritiva recebem nota de licença.

## R13. Figuras no texto

- Toda figura é citada no texto ("(Figura 3.4)") antes ou perto dela.
- Legenda é uma frase completa que diz o que a figura mostra **e** a conclusão.
- Detalhes em `FIGURAS.md`.

## R14. Restrições da ficha

Confidencialidade, fontes proibidas e cuidados éticos da ficha valem para tudo: exemplos, código, dados, figuras e casos. Na dúvida, não use.

---

## Lista de verificação rápida por seção

- [ ] Algum trecho conta como o texto foi feito? (R1)
- [ ] Algum arquivo ou ferramenta interna citada? (R2)
- [ ] Cada número tem origem e passos visíveis? Cada conversão é um passo? (R5)
- [ ] Bases, cenários e separadores coerentes? (R6)
- [ ] Mais de três siglas num parágrafo, ou sigla criada pelo livro? (R7)
- [ ] Tabelas com uma informação por coluna, sem parágrafos, com texto antes e depois? (R8)
- [ ] Toda fórmula e todo código explicados? (R9, R10)
