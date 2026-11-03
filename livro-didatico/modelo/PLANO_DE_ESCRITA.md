# Plano de escrita — {{TITULO}}

*Aprovar com o autor antes de escrever o primeiro capítulo. Guias: `guia/PEDAGOGIA.md` e `guia/PRODUCAO.md`.*

## Contexto

{{o que existe (documento de origem) e o que o livro acrescenta}}

## Decisões de formato

- Idioma: {{IDIOMA}}; equivalentes no glossário: {{idiomas}}.
- Volume: {{páginas por capítulo}}; ritmo de leitura: {{horas por capítulo}}.
- Fonte única em Markdown; PDF via LaTeX e Word.

## Caso condutor

| Elemento | Parâmetros | Capítulos em que aparece |
| --- | --- | --- |
| {{elemento}} | {{valores e unidades}} | {{1, 3, 5}} |

## Espiral: conceitos que voltam

| Conceito | Introduzido | Retomado em |
| --- | --- | --- |
| {{conceito}} | {{cap. 1}} | {{caps. 3, 5, 7}} |

## Capítulo a capítulo

### Capítulo 0 — Fundamentos (opcional, pré-requisitos)

### Capítulo 1 — {{título}}

- **Pergunta de abertura:** {{caso real, datado, com números}}
- **Objetivos (Bloom):** {{lembrar …, aplicar …, criar …}}
- **Seções:** 1.0 revisão rápida; 1.1 {{tema}}: fórmulas centrais, exemplo resolvido, estresse, caso histórico; 1.2 …
- **Laboratório:** {{o que o leitor constrói}}
- **Exercícios:** A {{…}}; B {{…}}; C {{…}}
- **Desafio integrador e entregável:** {{…}}
- **Dados abertos usados:** {{fonte, acesso}}
- **Fatos a verificar:** {{item (verificar)}}

## Apêndices

| Apêndice | Conteúdo |
| --- | --- |
| A | Matemática e estatística de apoio |
| B | Trilha de programação: ambiente, versionamento, testes |
| C | Pipeline de dados: fontes abertas, acesso, tratamento |
| D | Rotina de estudo e leitura contínua |
| E | Linha do tempo dos casos citados |
| F | Glossário consolidado |
| G | Soluções dos exercícios e respostas das perguntas de recuperação |
| H | Bibliografia comentada |

## Fontes complementares

{{livros-texto e artigos de referência por área}}

## Verificação

- Cada número do texto bate com a saída do código correspondente (rodado do zero, sementes fixas).
- Cada caso e cada regra têm fonte primária; nenhum `(verificar)` restante.
- Cada capítulo cobre o que o plano prevê.
- `ferramentas/verificar_livro.py` sem erros; páginas renderizadas inspecionadas.
