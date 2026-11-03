---
description: Inicia um livro-texto didático novo (entrevista, ficha, plano e criação do projeto)
argument-hint: "[pasta de destino] [tema]"
---

Inicie um livro-texto didático novo. Argumentos do usuário: $ARGUMENTS

1. Leia `${CLAUDE_PLUGIN_ROOT}/guia/PEDAGOGIA.md` (seções 1 a 4) e `${CLAUDE_PLUGIN_ROOT}/modelo/FICHA_DO_LIVRO.md`.
2. **Entreviste o usuário** para preencher a ficha: leitor, conhecimento prévio, objetivo final, nível, idioma, ritmo e volume, caso condutor (fictício), fontes de dados abertas, ferramentas de código, restrições, data de referência. Faça poucas perguntas por vez; proponha respostas padrão quando o usuário não tiver preferência.
3. Verifique o ambiente: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verificar_ambiente.py`. Se faltar algo, mostre o que falta, de onde viria e o comando, e **peça permissão** antes de instalar.
4. Crie o projeto: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/novo_livro.py DESTINO --titulo "…" --subtitulo "…" --autor "…" --data "…" --idioma …`. O script nunca sobrescreve arquivos.
5. Preencha `FICHA_DO_LIVRO.md` com as respostas e escreva o `PLANO_DE_ESCRITA.md` seguindo o modelo, com fatos de memória marcados `(verificar)`.
6. **Peça a aprovação do plano** antes de escrever qualquer capítulo.
7. Registre na `MEMORIA_DO_PROJETO.md` a ficha resumida, as decisões e as pendências.
