# Guia de produção: processo, diagramação, verificação e revisão

---

## 1. Visão geral do processo

1. **Ficha do livro** (`FICHA_DO_LIVRO.md`), preenchida numa conversa com o autor.
2. **Plano de escrita** (`PLANO_DE_ESCRITA.md`), aprovado pelo autor antes de escrever.
3. **Projeto criado** com `novo_livro.py` (estrutura, guias, ferramentas, modelos) e ambiente verificado.
4. **Um capítulo por rodada**, no ciclo da seção 3.
5. **Anotações de correção** registradas sempre que o autor ler e apontar problemas.
6. **Revisão final com três revisores independentes** (seção 6).
7. **Fechamento** com a lista da seção 7.

A memória do projeto (`MEMORIA_DO_PROJETO.md`) é atualizada ao fim de cada rodada: é o que permite retomar numa sessão nova.

---

## 2. Plano de escrita

Conteúdo mínimo:

- contexto: o que existe (documento de origem, ementa) e o que falta;
- decisões de formato: idioma, volume estimado por capítulo, ritmo de leitura;
- o caso condutor completo;
- capítulo a capítulo: pergunta de abertura, seções, fórmulas centrais, exemplos resolvidos, estresses, casos históricos, laboratório, exercícios e entregável;
- espiral: que conceitos voltam em que capítulos;
- fatos a verificar, marcados `(verificar)`;
- fontes de dados abertas previstas, com o modo de acesso;
- apêndices e fontes complementares.

---

## 3. Ciclo de cada capítulo

1. **Pesquisa e verificação.** Regras, datas e números em fonte primária. Leia o texto original: um prazo lido em resumo ("até 15 anos") pode ser outro no texto ("metade da vida útil, até 15 anos") e mudar toda a cadeia de números.
2. **Dados.** Scripts de download versionados; brutos e processados separados; licença registrada.
3. **Cálculo.** Um script por exemplo ou tabela em `codigo/capNN/`, com semente fixa; verificação por caminho independente.
4. **Redação.** Modelo de capítulo (`PEDAGOGIA.md`, seções 4 e 5) e regras de escrita (`ESCRITA.md`).
5. **Figuras.** `codigo/figuras/fig_capNN.py`; inserir com legenda completa; citar no texto; **abrir cada imagem**.
6. **Exercícios e gabaritos.** A/B/C, desafio, entregável, `apendices/G-solucoes-capNN.md` e `apendices/G-recuperacao-capNN.md`.
7. **Geração e checagem.** `gerar_livro.py`, `verificar_livro.py`, `amostrar_paginas.py`, e olhar as páginas.
8. **Memória.** Números-chave, decisões, pendências.

---

## 4. Pipeline de geração

### 4.1 Ferramentas

| Ferramenta | Papel | Licença |
| --- | --- | --- |
| pandoc | Markdown → LaTeX e Markdown → DOCX | GPL |
| Tectonic (motor XeTeX) | Compila o LaTeX; baixa pacotes e fontes sob demanda | MIT |
| Fontes Libertinus e DejaVu | Texto, matemática e código; carregadas por nome de arquivo | OFL / livre |
| Python 3.11+ | Scripts de cálculo, figuras e ferramentas do livro | PSF |
| poppler (`pdftoppm`, `pdfinfo`, `pdfimages`, `pdftotext`) | Inspeção do PDF | GPL |

### 4.2 Por que esta cadeia

| Opção | Qualidade | Custo | Veredito |
| --- | --- | --- | --- |
| Markdown → LaTeX (Tectonic) → PDF, mais Markdown → DOCX | Melhor diagramação de fórmulas, sumário e cabeçalhos | Um comando | **Recomendada** |
| PDF exportado do Word | Fórmulas e paginação piores | Manual | Evitar |
| Markdown → Typst → PDF | Boa, mas exige pós-processamento próprio | Duplica o trabalho | Dispensável |
| HTML | Bom para leitura no navegador | Extra | Só se pedido |

### 4.3 O que `gerar_livro.py` faz

1. Lê `livro.toml` (título, idioma, capítulos, apêndices).
2. Monta os apêndices; o G junta soluções e respostas de recuperação, capítulo a capítulo.
3. Concatena metadados, pré-textuais, capítulos (arquivos de cada `capNN/` em ordem alfabética) e apêndices em `build/livro.md`.
4. Gera `build/livro.tex` com o pandoc (classe `book`, capítulo como divisão de topo, sumário, filtro Lua, preâmbulo).
5. Compila com o Tectonic; copia para `saida/livro.pdf`.
6. Gera `saida/livro.docx`.

### 4.4 Decisões de diagramação (e por quê)

- **Figuras fixas no ponto do texto** (`\floatplacement{figure}{H}`): com figuras flutuantes, o LaTeX desloca e chega a **perder** figuras entre páginas.
- **Legendas sem rótulo automático** (`labelformat=empty`): o número já vem no texto da legenda.
- **Caixas com filete lateral** (`framed`), que quebram entre páginas.
- **Código com quebra de linha automática** (`fvextra`); blocos sem linguagem passam pelo filtro Lua. A opção `breaknonspaceingroup` não existe na versão do Tectonic.
- **Símbolos sem glifo** (✓, ☐) definidos com `\newunicodechar`.
- **Tabelas longas** em corpo menor, com `\emergencystretch` e `microtype`.
- **Fontes por nome de arquivo**, para funcionar sem fontes instaladas no sistema.

---

## 5. Verificação automática e visual

`ferramentas/verificar_livro.py` checa:

| Grupo | O que procura |
| --- | --- |
| Log do LaTeX | "Missing character" (glifo ausente), "Overfull \vbox" (página estourada), "Overfull \hbox" acima de 20 pt |
| Figuras | Arquivo inexistente; figura não citada; contagem no PDF diferente da do texto |
| Código | Bloco sem linguagem; bloco sem "Lendo o código" |
| Fórmulas | Espaço junto ao cifrão; acento em subscrito sem `\text{}`; fórmula destacada sem "Lendo a fórmula" (aviso) |
| Números | Ponto decimal no texto, hífen como sinal de menos, moeda com cifrão sem escape |
| Siglas | Sigla fora da lista; sigla sem expansão na primeira ocorrência do capítulo; parágrafo com mais de três siglas |
| Tabelas | Célula longa (parágrafo em tabela); coluna que mistura número e texto; tabela sem texto antes |
| Texto | Vazamento de processo; referência a arquivo interno; marcadores `{{…}}`, `(verificar)`, `TODO` |
| Gabaritos | Número de respostas diferente do de perguntas em cada capítulo |

Depois, **olhe as páginas**: `amostrar_paginas.py` renderiza a capa, o sumário, a abertura de cada capítulo e páginas sorteadas. Inclua pelo menos uma página com fórmula longa, uma com tabela larga, uma com código, uma com figura grande e uma do Apêndice G.

---

## 6. Revisão final com três revisores independentes

Ao terminar todos os capítulos, rode três agentes em paralelo, sem acesso às conclusões uns dos outros. Cada achado tem identificador, local, gravidade, evidência e correção proposta. Nenhum revisor corrige nada.

| Revisor | Olhar | Prefixo |
| --- | --- | --- |
| `revisor-visual` | Editor de arte de revista científica de primeira linha: figuras, legendas, diagramação, consistência visual | V- |
| `revisor-conteudo` | Especialista sênior da área: erros técnicos, números, regras, hipóteses, omissões, casos históricos | C- |
| `revisor-leitor` | Leitor-alvo da ficha: passos faltando, números sem origem, siglas, tabelas confusas, vazamentos, referências internas | L- |

**Tratamento dos achados:**

- Verifique cada achado antes de aceitar; revisores também erram. Refute com fonte quando for o caso.
- Se a correção mexe num número, refaça a cadeia e busque todas as ocorrências.
- Registre na memória o que foi aceito, o que foi refutado e por quê.
- Gere o livro de novo e repita as verificações.

---

## 7. Fechamento: lista final

- [ ] `verificar_livro.py` sem erros; avisos revistos um a um.
- [ ] Siglas: lista atualizada; nenhuma sigla criada pelo livro; nenhuma sopa de siglas.
- [ ] Código: todo bloco com linguagem e "Lendo o código"; toda fonte de dados com o código de acesso.
- [ ] Fórmulas: toda fórmula nova com "Lendo a fórmula"; zero "Missing character".
- [ ] Contas: todo exemplo com origem das entradas, todos os passos e conversões explícitas.
- [ ] Figuras: todas citadas, todas no PDF, todas inspecionadas.
- [ ] Gabaritos: respostas = perguntas; soluções de A, B e C em todos os capítulos.
- [ ] Vazamentos e referências internas: zero.
- [ ] Números-chave da memória iguais no texto, nas tabelas, nas figuras e nos gabaritos.
- [ ] Fatos: nenhum `(verificar)`; toda regra e caso com fonte e data.
- [ ] Restrições da ficha respeitadas.
- [ ] `ANOTACOES_CORRECAO.md` sem pendências.
- [ ] PDF e DOCX finais gerados; páginas por amostragem inspecionadas.
- [ ] Ambiente congelado (`requirements-lock.txt`); README e memória atualizados.

---

## 8. Lições aprendidas

1. **Ler a norma original**, não o resumo.
2. **Validar a fonte de dados contra a oficial** numa amostra, e registrar.
3. **Figuras flutuantes no LaTeX somem.** Fixe-as no lugar.
4. **Scripts que editam texto em massa podem corrompê-lo** (um normalizador de cifrão escapou moedas dentro de fórmulas). Revise o diff.
5. **Geradores não sobrescrevem texto escrito à mão:** gere só entre marcadores (`<!-- início gerado -->` … `<!-- fim gerado -->`).
6. **No zsh, `echo '\u...'` corrompe arquivos.** Escreva arquivos com Python ou com a ferramenta de escrita.
7. **Avaliar fora da amostra.** Resultados dentro da amostra podem inverter fora dela; mostre os dois.
8. **Um parâmetro de calibração fora da faixa física é um diagnóstico**, não uma solução.
9. **"Nota honesta"** para o que não foi feito.
10. **Gabaritos e explicações de código não são opcionais**; planeje-os desde o primeiro capítulo.
11. **O autor, lendo, encontra o que os scripts não encontram:** número sem origem (um coeficiente tirado do meio de uma faixa, ou uma diferença de temperaturas, sem dizer de onde vêm), conversão implícita (um ×10 escondido numa mudança de base de 0,1 unidade), derivada sem a forma equivalente nem a versão para variação finita. Registre em `ANOTACOES_CORRECAO.md` e procure o mesmo padrão no resto do livro.
12. **Textos gerados por script também são texto do livro**: um gerador de glossário escreveu "a tabela é gerada por `notebooks/…`" no apêndice, uma referência interna (R2).
