# Guia pedagógico

Como ensinar com o livro: os princípios, de onde vêm, e como cada um vira uma parte concreta do capítulo. Vale para qualquer assunto técnico (engenharia, finanças, estatística, ciência de dados, direito regulatório, medicina quantitativa…).

---

## 1. A ideia central: um livro construído com o leitor

O leitor não assiste ao livro; ele o percorre fazendo. Na prática:

- **Ele prevê antes de ver.** Antes de um resultado importante, o texto pede uma estimativa ("Antes de continuar: o custo médio sobe ou cai quando a produção dobra? Quanto?"). O erro de previsão é o que fixa o conceito.
- **Ele monta o caso condutor.** Um objeto fictício (empresa, sistema, paciente, carteira, planta, cidade) atravessa o livro. O leitor o constrói aos poucos: o número calculado no capítulo 2 é a entrada do capítulo 3.
- **Ele escreve o código.** O laboratório constrói, capítulo a capítulo, um pacote de código de verdade, com testes. No fim do livro, o leitor tem uma ferramenta, e não só anotações.
- **Ele confere.** Todo exercício de nível B tem um número de referência para o leitor comparar com o próprio resultado.
- **Ele é tratado como colega.** O texto fala com o leitor ("você", ou "nós" inclusivo), diz por que cada passo existe e admite o que o método não captura ("Nota honesta").

O teste: depois de cada seção, o leitor consegue refazer o exemplo sozinho, com outro número? Se não, falta passo.

---

## 2. Fundamentos (e o que cada um exige do texto)

| Princípio | Evidência | O que exige do livro |
| --- | --- | --- |
| Carga cognitiva | Sweller (1988); Sweller, Ayres e Kalyuga (2011) | Um conceito novo por vez; notação apresentada antes de ser usada; nenhum passo implícito; figuras ao lado do texto que explicam |
| Efeito do exemplo resolvido e retirada gradual do apoio | Renkl e Atkinson (2003); Sweller e Cooper (1985) | Primeiro exemplo de cada técnica resolvido por completo; o segundo deixa passos ao leitor; o terceiro vira exercício |
| Prática de recuperação | Roediger e Karpicke (2006); Brown, Roediger e McDaniel, *Make It Stick* (2014) | Perguntas curtas ao fim de cada seção, com gabarito comentado passo a passo |
| Espaçamento e intercalação | Cepeda et al. (2006); Rohrer e Taylor (2007) | Espiral: cada conceito central volta mais fundo em capítulos posteriores; exercícios que misturam técnicas |
| Elaboração e conhecimento prévio | Ambrose et al., *How Learning Works* (2010) | Caixa "Ponte com {{conhecimento prévio}}" que traduz o novo para o que o leitor já domina; revisão rápida com autoavaliação |
| Codificação dupla e princípios multimídia | Paivio (1971); Mayer, *Multimedia Learning* (2009) | Toda relação mencionada tem figura; texto e figura juntos (contiguidade); nada decorativo (coerência); valores marcados na figura (sinalização) |
| Concretude antes da abstração | Fyfe et al. (2014), *concreteness fading* | Intuição e caso concreto antes da fórmula geral |
| Objetivos mensuráveis | Anderson e Krathwohl (2001), Bloom revisada; Wiggins e McTighe, *Understanding by Design* (2005) | Objetivos por nível de Bloom no início; exercícios e entregável alinhados a esses objetivos (planejamento reverso) |
| Metacognição | Ambrose et al. (2010) | Autoavaliação na revisão rápida; checklist do laboratório; "o que o exemplo ensina" ao fim de cada exemplo |
| Prática deliberada e transferência | Ericsson et al. (1993) | Estresses ("e se?") e casos de outros lugares e épocas: o mesmo conceito em contextos diferentes |

---

## 3. Antes de escrever: o leitor e o plano

1. **Ficha do livro** (`FICHA_DO_LIVRO.md`): quem é o leitor, o que ele já sabe, o que precisa fazer ao final, quanto tempo tem, em que nível escrever. Toda decisão didática se apoia nela.
2. **Planejamento reverso:** comece pelo que o leitor deve **fazer** ao final de cada capítulo (o entregável). Os objetivos derivam do entregável; as seções derivam dos objetivos.
3. **Mapa de dependências:** quais conceitos cada capítulo pressupõe e quais retoma (espiral). Registre no plano e mostre ao leitor no prefácio.
4. **Capítulo 0 e Apêndice A** cobrem os pré-requisitos (fundamentos da área e a matemática de apoio), para o livro ser autocontido sem obrigar todos a lê-los.
5. **Caso condutor:** defina-o no plano, com nome fictício que não imite entidade real, parâmetros completos e a ordem em que cada parte aparece.

---

## 4. Anatomia do capítulo (e para que serve cada parte)

| Parte | Função didática | Forma |
| --- | --- | --- |
| Pergunta de abertura | Cria a necessidade do conteúdo | Caso real, datado, com números; 2 a 4 perguntas que o capítulo responde |
| Objetivos de aprendizagem | Diz o que o leitor saberá fazer | Tabela Nível de Bloom → objetivo com verbo mensurável (calcular, derivar, comparar, projetar, criticar) |
| Pré-requisitos | Evita que o leitor se perca | Lista curta, apontando o capítulo 0 ou o apêndice A |
| Mapa do capítulo | Organiza antes de detalhar | Seções e setas de dependência |
| O caso condutor neste capítulo | Ancora tudo num objeto concreto | Tabela com os elementos usados e de onde vêm os números (capítulo anterior) |
| Notação do capítulo | Reduz carga cognitiva | Tabela Símbolo / Como se lê / Significado / Unidade / Exemplo |
| N.0 Revisão rápida | Nivela; ativa o conhecimento prévio | Autoavaliação no topo ("se acertar tudo, leia na diagonal"), definições centrais, perguntas de recuperação |
| N.1 … N.k Seções avançadas | O conteúdo | Sequência da seção 5 |
| Laboratório | Transforma em habilidade | Tutorial de código passo a passo, com "Lendo o código", tarefas e checklist |
| Exercícios A/B/C | Prática graduada | Seção 8 |
| Desafio integrador e entregável | Transferência para o trabalho real | Problema aberto e um produto profissional |
| Resumo, fórmulas-chave, mapa de conceitos, glossário, leituras guiadas, fontes | Consolidação e continuidade | Tabelas e listas curtas |

---

## 5. A sequência dentro de cada seção

1. **Intuição.** A ideia sem fórmula, com um exemplo concreto do caso condutor. Uma pergunta de previsão.
2. **Formalização.** A definição precisa e a fórmula, seguida de **"Lendo a fórmula"** (seção 6).
3. **Derivação.** A prova ou dedução, em passos numerados com a conta de cada passo. Se for longa, numa caixa "Derivação".
4. **Exemplo resolvido.** Seção 7.
5. **Estresse.** Tabela "e se?" (seção 7.3).
6. **Caso histórico.** Um episódio real de outro lugar ou época, com números, fonte e lições.
7. **Armadilhas.** Erros comuns de praticantes, com o tamanho do erro em número.
8. **Perguntas de recuperação.** 3 a 5, com gabarito no apêndice.

Nem toda seção precisa de todas as partes, mas a ordem não muda: concreto → formal → aplicado → testado → lembrado.

---

## 6. Notação e fórmulas como ensino

- **Toda fórmula nova** é seguida de uma caixa `> **Lendo a fórmula.**` (ou `Lendo a notação`) com:
  1. cada símbolo: como se lê em voz alta, o que é, unidade;
  2. operadores menos comuns explicados na primeira vez ($(x)^+$, $\mathbf 1\{\cdot\}$, $\min$, somatório com índice);
  3. um exemplo numérico curto, com todos os passos;
  4. a leitura do significado ("o desconto é uma covariância", "cada unidade extra só rende nos períodos em que ainda há folga").
- **Derivadas e variações:** quando a fórmula é uma taxa marginal, mostre a derivada termo a termo, uma forma equivalente que deixe explícito o que é descontado, e a versão para variação finita, com um exemplo em que as duas diferem.
- **Resultados centrais** em caixa (`\boxed{}`) e repetidos na tabela de fórmulas-chave do fim do capítulo.

---

## 7. Exemplos resolvidos

### 7.1 Anatomia

```markdown
**Exemplo resolvido — {{título que diz a pergunta}}.**

*Dados.* {{tabela ou lista, com unidade e origem de cada valor}}

**Passo 1 — {{o que se faz}}.** {{fórmula com os números substituídos}} = **{{resultado com unidade}}**.

**Passo 2 — …**

*Verificação.* {{o mesmo resultado por outro caminho}}

*O que o exemplo ensina.* (1) … (2) …
```

### 7.2 Regras

- **Cada número de entrada tem origem dita:** do enunciado, de um capítulo anterior, de uma fonte, ou de uma escolha ("usamos 0,35%/°C, o meio da faixa de 0,30% a 0,40%").
- **Cada passo tem uma operação.** Conversões de unidade e de base são passos próprios ("o passo acrescenta 0,1 sensor por central; por sensor: 12,5 / 0,1 = 125 €").
- **Verificação por caminho independente** sempre que possível: dualidade, paridade, simulação contra fórmula fechada, conta à mão contra o solver.
- **Orientação decrescente:** completo → com lacunas ("complete o passo 3") → exercício.
- **O exemplo usa o caso condutor ou dados reais**, nunca números soltos sem contexto.

### 7.3 Tabela de estresse

| Mudança | Efeito em {{métrica}} | Mecanismo |
| --- | --- | --- |
| {{variante do objeto}} | {{número}} | {{por quê}} |
| {{choque de entrada}} | | |
| {{evento regulatório ou institucional}} | | |
| {{evento raro}} | | |

O texto antes da tabela diz o que se varia; o texto depois diz qual mudança domina e por quê.

---

## 8. Perguntas, exercícios e gabaritos

### 8.1 Perguntas de recuperação

- 3 a 5 por seção, numeradas, curtas, mistura de conceito e conta.
- Logo abaixo do título: `*Respostas comentadas no Apêndice G.*`
- Gabarito no Apêndice G, **passo a passo**:

```markdown
**1. {{pergunta resumida}}**

*Passo 1 — {{o que se faz}}.* {{conta ou raciocínio}}

*Passo 2 — …* **{{resultado}}**.

*Passo 3 — a leitura.* {{o que o número significa}}
```

- Se a resposta exige um número que o livro não tem, ele é calculado em código antes.

### 8.2 Exercícios

| Nível | O que treina | Formato |
| --- | --- | --- |
| **A — fixação** | Cálculo à mão, definição, leitura de fórmula | Dados pequenos (3 a 24 valores), itens a), b), c) |
| **B — aplicação** | Uso de dados reais e do código do laboratório | Número de referência para conferir |
| **C — aprofundamento** | Derivação, extensão de modelo, crítica de artigo, replicação de figura | Roteiro de solução, não a solução inteira |
| **Desafio integrador** | Junta o capítulo inteiro | Problema aberto |
| **Entregável** | Transferência para o trabalho | Produto profissional (nota de uma página, modelo, relatório) |

Soluções no Apêndice G: completas para A, números de referência para B, roteiros para C.

---

## 9. Caixas recorrentes

São citações em Markdown (`> **Título.** …`), que viram caixas com filete lateral.

| Caixa | Quando usar |
| --- | --- |
| **Lendo a fórmula** / **Lendo a notação** | Depois de toda fórmula nova |
| **Lendo o código** | Depois de todo bloco de código |
| **Intuição** | A ideia antes da fórmula |
| **Derivação** | Prova longa |
| **Caso histórico — {{lugar, data}}: {{título}}** | Episódio real com números, fonte e "Lições: (1)… (2)…" |
| **Armadilha — {{nome}}** | Erro comum, com o tamanho do erro |
| **Ponte com {{conhecimento prévio}}** | Tradução para o que o leitor já domina |
| **Na prática** (ou **Na {{organização do leitor}}**) | Como o tema aparece no trabalho real |
| **Nota honesta** | O que o livro simplificou ou não fez, e o efeito disso |
| **Autoavaliação** | Início da revisão rápida |
| **Antes de continuar** | Pergunta de previsão |

---

## 10. Casos históricos

- **Variedade:** outros países, épocas e setores; crises, choques, falhas, mudanças de regra, sucessos e fracassos.
- **Estrutura:** contexto (data, lugar) → o que aconteceu, com números → por quê (mecanismo) → lições numeradas que voltam ao conceito da seção.
- **Fonte primária ou de alta qualidade**, citada com data no fim do capítulo.

---

## 11. Profundidade

- O nível vem da ficha. Para mestrado: derivações completas, estado da arte com autores e anos, crítica do que o método não captura.
- Nada superficial: cada conceito central passa pela sequência inteira da seção 5.
- Dados reais e recentes sempre que possível, com o código que os obtém.

---

## 12. Como avaliar se a didática funcionou

Antes de dar um capítulo por pronto, leia como o leitor (o agente `revisor-leitor` faz isso):

- [ ] Consigo refazer cada exemplo com outro número, só com o que está escrito?
- [ ] Cada número tem origem visível? Cada conversão de unidade ou de base é um passo?
- [ ] Cada símbolo foi explicado antes ou logo depois de aparecer?
- [ ] Há alguma sigla que precisei procurar?
- [ ] Cada figura é citada e diz algo que o texto não diz sozinho?
- [ ] As perguntas de recuperação cobrem os objetivos de aprendizagem?
- [ ] O entregável exige exatamente o que os objetivos prometem?

Os problemas encontrados na leitura do autor viram itens de `ANOTACOES_CORRECAO.md`.
