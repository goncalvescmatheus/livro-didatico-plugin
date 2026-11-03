# CLAUDE.md — projeto de livro-texto didático

Este projeto produz um **livro-texto técnico e didático**. A fonte é Markdown; as saídas são PDF (via LaTeX) e Word. Estas regras valem para toda sessão neste projeto e têm prioridade sobre hábitos padrão.

## Leia antes de trabalhar

1. `FICHA_DO_LIVRO.md`: leitor, nível, caso condutor, restrições, data de referência.
2. `MEMORIA_DO_PROJETO.md`: estado, decisões, números-chave e pendências. **Atualize-a ao fim de cada rodada.**
3. `ANOTACOES_CORRECAO.md`: correções pendentes vindas da leitura do autor.
4. Os guias, quando a tarefa tocar no assunto deles:
   - `guia/PEDAGOGIA.md`: a abordagem didática e a anatomia do capítulo;
   - `guia/ESCRITA.md`: estilo e restrições de texto (as regras R1 a R14);
   - `guia/REPRODUTIBILIDADE.md`: números, dados, código e preferência por ferramentas abertas;
   - `guia/FIGURAS.md`: regras das figuras;
   - `guia/PRODUCAO.md`: pipeline, diagramação, verificação e revisão.

## Regras inegociáveis

1. **O texto é para o leitor, não sobre o processo.** Nada de vazamento de pensamento ou de elaboração ("corrigimos", "na versão anterior", "vou calcular", "como discutido", "nesta sessão", "o modelo errou porque eu"). Escreva conhecimento estabelecido, dirigido ao leitor.
2. **Autocontido.** O livro nunca se refere a arquivos, pastas ou ferramentas internas do projeto (`codigo/`, `build/`, `MEMORIA…`, "gerado por script X"). Só cita arquivos que o próprio leitor cria seguindo o laboratório. Todo dado vem com o código que o obtém; todo termo é definido no livro.
3. **Construído com o leitor.** O leitor faz junto: prevê antes de ver o resultado, monta o caso condutor, escreve o código do laboratório, confere números. Os resultados de um capítulo alimentam o seguinte.
4. **Toda conta com todos os passos.** Diga de onde vem cada número de entrada, mostre cada operação e cada conversão de unidade ou de base, e o resultado com unidade. Nenhum "ou seja, 125 €" sem a divisão que leva a ele.
5. **Todo número vem de código executado.** Calcule antes de escrever, com semente fixa; texto, tabelas, figuras e gabaritos usam o mesmo número. Se uma premissa mudar, refaça a cadeia e procure o número antigo em todos os arquivos.
6. **Números sem mistura.** Uma base por cálculo (por unidade instalada × por unidade de capacidade, por ano × por mês, nominal × real); separadores do idioma (no português: vírgula decimal, ponto de milhar, sinal de menos "−"); unidades explícitas.
7. **Siglas com parcimônia.** Escreva por extenso; sigla só se for padrão da área e frequente. Nunca crie siglas para conceitos do livro. Expanda na primeira ocorrência de cada capítulo e registre em `0s-siglas.md`.
8. **Tabelas limpas.** Uma informação por coluna, unidade no cabeçalho, nada de parágrafos em células, texto antes (o que a tabela mostra) e depois (o que se conclui).
9. **Toda fórmula nova tem "Lendo a fórmula"; todo bloco de código tem "Lendo o código".**
10. **Fatos verificados em fonte primária**, com data e referência no fim do capítulo. O que veio de memória fica marcado `(verificar)` até ser conferido e nunca chega à versão final.
11. **Preferência por ferramentas abertas:** pacotes de código aberto, dados abertos, modelos abertos e APIs públicas. Ferramenta proprietária só se não houver alternativa, e então com nota de acesso.
12. **Restrições da ficha** (confidencialidade, fontes proibidas) valem para texto, código, dados e figuras.

## Ferramentas e permissão

- Verifique o ambiente com `python3 ferramentas/verificar_ambiente.py`.
- **Nunca instale nada sem pedir permissão ao usuário no chat**, dizendo o quê, de onde e o comando. Só depois do "sim", rode `python3 ferramentas/verificar_ambiente.py --instalar --sim` ou o comando específico.
- Python em ambiente virtual próprio (`.venv`), com as versões de `requirements.txt`.

## Comandos do dia a dia

```bash
python3 ferramentas/novo_capitulo.py 3 "Título do capítulo"    # cria cap03/, gabaritos e pastas
python3 ferramentas/gerar_livro.py                             # PDF (LaTeX/Tectonic) e DOCX em saida/
python3 ferramentas/verificar_livro.py                         # checagens de texto, siglas, tabelas, números, log
python3 ferramentas/amostrar_paginas.py                        # renderiza páginas do PDF para inspeção visual
```

## Ciclo de cada capítulo

pesquisar e verificar fontes → baixar dados com script → calcular em código → escrever seguindo o modelo → gerar e inspecionar figuras → exercícios e gabaritos → gerar o livro → `verificar_livro.py` → olhar páginas renderizadas → atualizar a memória.

## Anotações de correção

Quando o usuário apontar um problema de leitura (passo faltando, número sem origem, notação obscura), registre em `ANOTACOES_CORRECAO.md` com arquivo e linha, o problema e o texto proposto, a menos que ele peça para corrigir na hora. Ao aplicar, marque como feito e verifique se o mesmo padrão aparece em outros capítulos.
