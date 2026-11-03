---
description: Cria e escreve um capítulo no ciclo completo (pesquisa, cálculo, texto, figuras, gabaritos, geração, verificação)
argument-hint: "N \"Título do capítulo\""
---

Escreva o capítulo pedido: $ARGUMENTS

1. Leia `CLAUDE.md`, `FICHA_DO_LIVRO.md`, `PLANO_DE_ESCRITA.md` (a parte do capítulo), `MEMORIA_DO_PROJETO.md` e `ANOTACOES_CORRECAO.md`; depois `guia/PEDAGOGIA.md`, `guia/ESCRITA.md` e `guia/REPRODUTIBILIDADE.md`.
2. Crie a estrutura: `python3 ferramentas/novo_capitulo.py N "Título"`. Crie arquivos de seção adicionais copiando `01_secao.md` (`02_…`, `03_…`).
3. **Pesquise e verifique** regras, datas, números e casos em fonte primária; registre as fontes.
4. **Dados:** scripts de download em `codigo/capNN/`; registre em `dados/FONTES.md`. Prefira dados e ferramentas abertos.
5. **Calcule** cada exemplo, tabela e gabarito em `codigo/capNN/` (semente fixa), com verificação por caminho independente. Anote os números-chave na memória.
6. **Escreva** seguindo o modelo; aplique as regras R1 a R14 de `guia/ESCRITA.md`, com atenção a: contas com todos os passos e a origem de cada entrada; nenhuma referência interna; siglas mínimas; tabelas limpas.
7. **Figuras** com `codigo/figuras/fig_capNN.py` e `estilo.py`; abra e inspecione cada imagem; cite cada uma no texto.
8. **Exercícios e gabaritos:** A/B/C, desafio, entregável; `apendices/G-solucoes-capNN.md` e `apendices/G-recuperacao-capNN.md`, com uma resposta passo a passo por pergunta.
9. Rode `python3 ferramentas/gerar_livro.py`, `python3 ferramentas/verificar_livro.py` e `python3 ferramentas/amostrar_paginas.py`; olhe as páginas do capítulo; corrija até não haver erros.
10. Leia o capítulo como o leitor (lista da seção 12 de `guia/PEDAGOGIA.md`) e atualize a memória.
