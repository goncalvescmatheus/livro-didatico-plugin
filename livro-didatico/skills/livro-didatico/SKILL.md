---
name: livro-didatico
description: >
  Planeja, escreve, diagrama e verifica livros-texto técnicos e didáticos sobre qualquer assunto, construídos com
  o leitor: capítulos com intuição, fórmula comentada, exemplo resolvido passo a passo, estresse, casos históricos,
  perguntas de recuperação com gabarito e exercícios em três níveis; números reproduzíveis por código; PDF via LaTeX
  e Word a partir de Markdown. Use quando o usuário quiser criar, continuar, revisar ou gerar um livro-texto,
  apostila, manual didático ou material de curso em capítulos, ou quando o projeto tiver livro.toml e CLAUDE.md
  deste plugin.
---

# Livro-texto didático

O plugin tem guias, modelos e ferramentas. A raiz do plugin fica dois níveis acima deste arquivo (`../../`); dentro de um projeto já criado, as mesmas coisas estão copiadas em `guia/`, `ferramentas/` e `CLAUDE.md`.

## Antes de tudo

1. **Projeto novo?** Siga `/livro-didatico:novo-livro`: entrevista para a ficha, plano de escrita, criação do projeto com `scripts/novo_livro.py`, verificação do ambiente.
2. **Projeto existente?** Leia `CLAUDE.md`, `FICHA_DO_LIVRO.md`, `MEMORIA_DO_PROJETO.md` e `ANOTACOES_CORRECAO.md` do projeto.
3. **Ferramentas:** rode `python3 ferramentas/verificar_ambiente.py`. **Nunca instale nada sem pedir permissão no chat**, dizendo o quê, de onde e o comando.

## Guias (leia o que a tarefa pede)

| Guia | Quando |
| --- | --- |
| `guia/PEDAGOGIA.md` | Planejar o livro ou um capítulo; escrever seções, exemplos, perguntas, exercícios |
| `guia/ESCRITA.md` | Qualquer texto para o leitor: regras R1 a R14 |
| `guia/REPRODUTIBILIDADE.md` | Calcular números, baixar dados, escolher pacotes, modelos e APIs |
| `guia/FIGURAS.md` | Gerar ou revisar figuras |
| `guia/PRODUCAO.md` | Gerar o livro, verificar, revisar, fechar |

## As regras que mais falham

1. Nenhum vazamento de pensamento ou de elaboração no texto.
2. Nenhuma referência a arquivos ou ferramentas internas do projeto: o livro é autocontido.
3. Toda conta com todos os passos: origem de cada entrada, cada conversão de unidade ou base como passo próprio.
4. Todo número sai de código executado, com semente fixa; o mesmo número em texto, tabela, figura e gabarito.
5. Siglas só as consagradas e frequentes, expandidas na primeira vez em cada capítulo; nunca siglas inventadas.
6. Tabelas: uma informação por coluna, unidade no cabeçalho, sem parágrafos, com texto antes e depois.
7. Não misturar bases, cenários ou separadores numéricos.
8. "Lendo a fórmula" depois de toda fórmula nova; "Lendo o código" depois de todo bloco.
9. Preferir pacotes, dados, modelos e APIs abertos.

## Fluxo de um capítulo

```text
pesquisar (fonte primária) → dados (script) → cálculo (codigo/capNN, semente fixa)
→ redação (modelo de capítulo) → figuras (estilo.py, abrir cada imagem)
→ exercícios + gabaritos (Apêndice G) → gerar_livro.py → verificar_livro.py
→ amostrar_paginas.py (olhar as páginas) → atualizar MEMORIA_DO_PROJETO.md
```

## Comandos do plugin

| Comando | Faz |
| --- | --- |
| `/livro-didatico:novo-livro` | Entrevista, ficha, plano e criação do projeto |
| `/livro-didatico:novo-capitulo N "Título"` | Cria e escreve um capítulo no ciclo completo |
| `/livro-didatico:gerar` | Gera PDF e Word e roda as verificações |
| `/livro-didatico:revisar` | Três revisores independentes (visual, conteúdo, leitor) |
| `/livro-didatico:anotar` | Registra uma correção apontada pelo autor |
| `/livro-didatico:aplicar-anotacoes` | Aplica as correções pendentes e procura o mesmo padrão no livro |
