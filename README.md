# livro-didatico

**Um plugin do Claude Code para escrever livros-texto técnicos e didáticos sobre qualquer assunto, do planejamento ao PDF final.**

Você descreve o leitor e o tema. O plugin conduz uma entrevista, monta o plano do livro, escreve capítulo por capítulo seguindo um método didático explícito, calcula cada número em código reproduzível, gera figuras, exercícios e gabaritos, diagrama o livro em PDF (via LaTeX) e Word, verifica automaticamente o resultado e o submete a três revisores independentes.

O método nasceu da produção de um livro-texto de nível de mestrado com mais de 400 páginas, 9 capítulos, 8 apêndices, cerca de 110 figuras e quase 200 perguntas de recuperação com gabarito comentado. Tudo o que foi aprendido nesse processo, inclusive os erros, virou regra, modelo ou verificação automática.

---

## O que o plugin entrega

- **Um método pedagógico explícito**, baseado em pesquisa sobre aprendizagem: carga cognitiva, exemplos resolvidos com retirada gradual do apoio, prática de recuperação, espiral de conceitos, codificação dupla e objetivos pela taxonomia de Bloom revisada.
- **Um livro construído com o leitor:** ele prevê resultados antes de vê-los, monta um caso condutor fictício ao longo dos capítulos e escreve o código que reproduz cada número.
- **Capítulos com estrutura fixa:** pergunta de abertura a partir de um caso real, objetivos, revisão rápida com autoavaliação e seções que vão da intuição à fórmula, da fórmula à derivação, ao exemplo resolvido, ao teste de estresse, ao caso histórico e às armadilhas. Cada capítulo fecha com laboratório de código, exercícios em três níveis, desafio integrador e entregável.
- **Contas sempre completas:** a origem de cada número de entrada, cada operação e cada conversão de unidade ou de base aparecem como passos próprios.
- **Reprodutibilidade:** todo número do texto sai de código executado, com semente fixa, e o mesmo número aparece no texto, nas tabelas, nas figuras e nos gabaritos. A preferência é sempre por pacotes, dados, modelos e APIs abertos.
- **Diagramação profissional** a partir de uma única fonte em Markdown: PDF com LaTeX (fórmulas, sumário, cabeçalhos, caixas, código com quebra de linha, figuras fixas no lugar) e Word.
- **Verificação automática** de dezenas de problemas que a leitura deixa passar (lista abaixo).
- **Revisão independente** por três agentes: um editor visual, um especialista da área e um leitor-alvo.

---

## Como um capítulo é organizado

```text
Capítulo N — Título
├── Pergunta de abertura        caso real, datado, com números
├── Objetivos de aprendizagem   um por nível de Bloom
├── Pré-requisitos, mapa, caso condutor, notação
├── N.0 Revisão rápida           autoavaliação + perguntas de recuperação
├── N.1 … N.k Seções
│   ├── Intuição                 com uma pergunta de previsão
│   ├── Formalização             fórmula + caixa "Lendo a fórmula"
│   ├── Derivação                passos numerados
│   ├── Exemplo resolvido        origem das entradas, passos, verificação
│   ├── Estresse                 tabela "e se?"
│   ├── Caso histórico           números, fonte, lições
│   ├── Armadilhas
│   └── Perguntas de recuperação (respostas passo a passo no Apêndice G)
├── Laboratório                  código + caixa "Lendo o código" + tarefas
├── Exercícios A / B / C, desafio integrador, entregável
└── Resumo, fórmulas-chave, glossário, leituras guiadas, fontes
```

Os apêndices padrão cobrem matemática de apoio, trilha de programação, pipeline de dados, rotina de leitura, linha do tempo dos casos, glossário consolidado, soluções e respostas, e bibliografia comentada. Todos são configuráveis.

---

## Instalação

### Pré-requisitos

| Ferramenta | Para quê |
| --- | --- |
| [Claude Code](https://docs.claude.com/en/docs/claude-code) | Terminal, app desktop ou extensão de IDE |
| Python 3.11 ou mais novo | Ferramentas do livro (só biblioteca padrão) e cálculos |
| [pandoc](https://pandoc.org) | Markdown → LaTeX e Word |
| [Tectonic](https://tectonic-typesetting.github.io) | Compila o PDF; baixa pacotes LaTeX e fontes na primeira execução |
| [poppler](https://poppler.freedesktop.org) (recomendado) | Renderiza páginas do PDF para inspeção visual |

Todos são gratuitos e de código aberto. Não é preciso instalá-los antes: o plugin verifica o ambiente, mostra o que falta e o comando de instalação para o seu sistema, e **só instala com a sua permissão**.

### Instalar o plugin

No Claude Code:

```text
/plugin marketplace add goncalvescmatheus/livro-didatico-plugin
/plugin install livro-didatico@instrucoes-livro
```

Para usar a partir de uma cópia local do repositório, troque `goncalvescmatheus/livro-didatico-plugin` pelo caminho da pasta.

---

## Uso

### Começar um livro

```text
/livro-didatico:novo-livro ~/livros/termodinamica "Termodinâmica aplicada"
```

Pedir em linguagem natural também funciona ("quero escrever um livro-texto de econometria para mestrandos"). O plugin então:

1. entrevista você para preencher a **ficha do livro**: leitor, conhecimento prévio, objetivo final, nível, idioma, ritmo, caso condutor, fontes de dados abertas, ferramentas e restrições;
2. verifica as ferramentas e pede permissão para instalar o que faltar;
3. cria o projeto com regras, guias, modelos e ferramentas;
4. escreve o **plano de escrita** e espera a sua aprovação antes do primeiro capítulo.

### Comandos

| Comando | O que faz |
| --- | --- |
| `/livro-didatico:novo-livro [pasta] [tema]` | Entrevista, ficha, plano e criação do projeto |
| `/livro-didatico:novo-capitulo N "Título"` | Ciclo completo de um capítulo: pesquisa em fontes primárias, dados, cálculo, texto, figuras, exercícios, gabaritos, geração e verificação |
| `/livro-didatico:gerar` | Gera o PDF e o Word, roda as verificações e renderiza páginas para inspeção |
| `/livro-didatico:revisar` | Revisão com três agentes independentes e tratamento dos achados |
| `/livro-didatico:anotar` | Registra um problema que você encontrou lendo, com o texto corrigido pronto, sem alterar o livro |
| `/livro-didatico:aplicar-anotacoes` | Aplica as correções registradas e procura o mesmo problema no resto do livro |

Dentro de um projeto, o arquivo `CLAUDE.md` carrega as regras do livro em toda sessão, de modo que o trabalho pode ser retomado a qualquer momento.

### Sem o Claude

As ferramentas também funcionam sozinhas:

```bash
python3 livro-didatico/scripts/novo_livro.py ~/meu-livro --titulo "Meu livro" --idioma pt-BR
cd ~/meu-livro
python3 ferramentas/novo_capitulo.py 1 "Primeiro capítulo"
python3 ferramentas/gerar_livro.py        # saida/livro.pdf e saida/livro.docx
python3 ferramentas/verificar_livro.py    # relatório de erros e avisos
python3 ferramentas/amostrar_paginas.py   # páginas em PNG para inspeção
```

---

## Regras de escrita

O guia de escrita traz 14 regras, cada uma com exemplo errado e certo. As principais:

1. **Nenhum vazamento de processo:** o texto apresenta conhecimento, nunca a história de como foi escrito.
2. **Autocontido:** o livro não se refere a arquivos ou ferramentas internas do projeto; todo dado vem com o código que o obtém.
3. **Construído com o leitor:** previsões, caso condutor, código escrito pelo leitor, números de referência para conferir.
4. **Toda conta com todos os passos,** incluindo a origem de cada entrada e cada conversão de unidade ou de base.
5. **Números sem mistura:** uma base e um cenário por cálculo; separadores do idioma em texto, tabelas e figuras.
6. **Siglas com parcimônia:** só as consagradas e frequentes; nunca siglas inventadas pelo livro.
7. **Tabelas limpas:** uma informação por coluna, unidade no cabeçalho, sem parágrafos nas células, com texto antes e depois.
8. **Toda fórmula e todo código explicados** nas caixas "Lendo a fórmula" e "Lendo o código".
9. **Fatos conferidos em fonte primária,** com data e referência.

---

## Verificação automática

`verificar_livro.py` separa erros (a corrigir) de avisos (a revisar):

| Grupo | O que encontra |
| --- | --- |
| Texto | Vazamentos de processo, referências a arquivos internos, marcadores não preenchidos, `(verificar)`, `TODO` |
| Números | Decimal com ponto no texto, hífen como sinal de menos, moeda com cifrão sem escape |
| Fórmulas | Espaço junto ao cifrão, acento em subscrito sem `\text{}`, fórmula sem explicação |
| Código | Bloco sem linguagem, bloco sem "Lendo o código" |
| Siglas | Sigla fora da lista, sem expansão na primeira ocorrência do capítulo, pouco usada, parágrafo com siglas demais |
| Tabelas | Parágrafo dentro de célula, coluna que mistura número e texto, tabela sem texto de introdução |
| Figuras | Arquivo inexistente, figura não citada, figura perdida no PDF |
| Gabaritos | Pergunta sem resposta, capítulo sem soluções ou sem fontes |
| LaTeX | Glifo ausente, página estourada, linha além da margem |

O que só a leitura encontra (um número sem origem, uma conversão implícita) fica a cargo do revisor-leitor.

## Revisão independente

| Agente | Olhar | Achados |
| --- | --- | --- |
| `revisor-visual` | Editor de arte de revista científica: figuras, legendas, diagramação, consistência | V-001… |
| `revisor-conteudo` | Especialista sênior da área: erros técnicos, números, regras, hipóteses, omissões | C-001… |
| `revisor-leitor` | Leitor-alvo: refaz cada conta e aponta passos faltando, notação obscura, siglas, tabelas confusas | L-001… |

Os três trabalham em paralelo e não alteram nada. Cada achado é verificado antes de ser aceito.

---

## Estrutura de um projeto de livro

```text
meu-livro/
├── CLAUDE.md                 regras do projeto
├── livro.toml                título, idioma, separadores, capítulos, apêndices
├── FICHA_DO_LIVRO.md         leitor, nível, caso condutor, restrições
├── PLANO_DE_ESCRITA.md       plano aprovado
├── MEMORIA_DO_PROJETO.md     estado, decisões, números-chave
├── ANOTACOES_CORRECAO.md     correções pendentes da sua leitura
├── 0p-prefacio.md, 0s-siglas.md
├── cap01/ … capNN/           um arquivo Markdown por bloco de seções
├── apendices/                A–H; o G é montado das soluções de cada capítulo
├── codigo/                   scripts que produzem cada número e cada figura
├── dados/                    brutos, processados e o registro de fontes
├── figuras/, latex/, guia/, ferramentas/
└── saida/                    livro.pdf e livro.docx
```

## Personalização

- **Idioma e números:** `idioma`, `decimal` e `milhar` em `livro.toml`. O padrão é português, com vírgula decimal.
- **Apêndices:** lista e ordem em `livro.toml`.
- **Verificações:** limites de siglas por parágrafo e de tamanho de célula, siglas ignoradas e padrões extras de vazamento em `livro.toml`.
- **Visual:** preâmbulo em `latex/cabecalho.tex`; cores por conceito em `codigo/figuras/estilo.py`.
- **Método:** os guias em `guia/` são texto puro e podem ser adaptados a cada projeto.

## Conteúdo deste repositório

| Caminho | Conteúdo |
| --- | --- |
| `.claude-plugin/marketplace.json` | Marketplace que publica o plugin |
| `livro-didatico/` | O plugin: regras, guias, skill, comandos, agentes, ferramentas e modelos (detalhes em `livro-didatico/README.md`) |
