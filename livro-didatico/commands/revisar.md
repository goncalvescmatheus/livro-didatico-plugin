---
description: Revisão final com três revisores independentes (visual, conteúdo e leitor), seguida do tratamento dos achados
argument-hint: "[capítulos ou 'todos']"
---

Revise o livro (escopo: $ARGUMENTS; padrão: todos os capítulos).

1. Garanta que o PDF está atualizado (`python3 ferramentas/gerar_livro.py`).
2. Lance **em paralelo** os agentes `revisor-visual`, `revisor-conteudo` e `revisor-leitor`, cada um com o caminho do projeto, o escopo e a ficha do livro. Eles não veem as conclusões uns dos outros e não corrigem nada.
3. Ao receber os relatórios, **verifique cada achado** antes de aceitar; refute com fonte quando for o caso.
4. Mostre ao usuário a lista consolidada (V-, C-, L-), com a sua decisão para cada um, e pergunte se pode aplicar.
5. Ao aplicar: se mexer num número, refaça a cadeia (código → figuras → tabelas → texto → gabaritos) e procure o número antigo em todos os arquivos. Achados de leitura que se repetem viram regra: procure o mesmo padrão no livro inteiro.
6. Gere de novo, verifique, e registre na memória o que foi aceito, refutado e por quê.
