# livro-didatico — plugin para escrever livros-texto técnicos e didáticos

Plugin do Claude Code para produzir livros-texto sobre **qualquer assunto técnico**, construídos com o leitor:

- capítulos com intuição, fórmula comentada, derivação, exemplo resolvido passo a passo, estresse, casos históricos e armadilhas;
- perguntas de recuperação com gabarito e exercícios em três níveis;
- números reproduzíveis por código, com preferência por ferramentas e dados abertos;
- PDF (via LaTeX) e Word a partir de uma fonte única em Markdown.

## Instalação

Pelo marketplace local (a pasta que contém `.claude-plugin/marketplace.json`):

```text
/plugin marketplace add /caminho/para/Instrucoes_Livro
/plugin install livro-didatico@instrucoes-livro
```

## Uso

| Comando | Faz |
| --- | --- |
| `/livro-didatico:novo-livro [pasta] [tema]` | Entrevista, ficha, plano e criação do projeto |
| `/livro-didatico:novo-capitulo N "Título"` | Ciclo completo de um capítulo |
| `/livro-didatico:gerar` | PDF, Word e verificações |
| `/livro-didatico:revisar` | Revisores visual, de conteúdo e leitor, em paralelo |
| `/livro-didatico:anotar` | Registra uma correção apontada na leitura |
| `/livro-didatico:aplicar-anotacoes` | Aplica as correções e generaliza para o livro todo |

Sem o plugin, os scripts funcionam direto: `python3 scripts/novo_livro.py ~/meu-livro --titulo "…"`.

## Conteúdo

| Caminho | O quê |
| --- | --- |
| `.claude-plugin/plugin.json` | Manifesto do plugin |
| `CLAUDE.md` | Regras do projeto (copiado para cada livro) |
| `REQUISITOS.md`, `requirements.txt` | Ferramentas, instalação por sistema e a regra de pedir permissão |
| `guia/PEDAGOGIA.md` | A abordagem didática detalhada e a anatomia do capítulo |
| `guia/ESCRITA.md` | Estilo e restrições (R1 a R14), com exemplos errado × certo |
| `guia/REPRODUTIBILIDADE.md` | Números por código, dados, ambiente, preferência por ferramentas abertas |
| `guia/FIGURAS.md` | Regras das figuras |
| `guia/PRODUCAO.md` | Processo, pipeline, diagramação, verificação, revisão, fechamento e lições aprendidas |
| `skills/livro-didatico/SKILL.md` | Skill que orienta o assistente |
| `commands/` | Os seis comandos |
| `agents/` | Revisores visual, de conteúdo e leitor |
| `scripts/` | Ferramentas (copiadas para `ferramentas/` em cada livro) |
| `modelo/` | Esqueleto do projeto: `livro.toml`, ficha, plano, memória, anotações, prefácio, siglas, apêndices, LaTeX, estilo de figuras |
| `modelo_capitulo/`, `modelo_apendice_g/` | Modelos de capítulo e de gabarito |

## Ferramentas (`scripts/`)

| Script | Faz |
| --- | --- |
| `verificar_ambiente.py` | Diz o que falta e como instalar; só instala com `--instalar` e permissão |
| `novo_livro.py` | Cria o projeto (nunca sobrescreve) |
| `novo_capitulo.py` | Cria `capNN/`, gabaritos, pastas e registra no `livro.toml` |
| `gerar_livro.py` | Monta a fonte única e gera PDF (pandoc + Tectonic) e DOCX |
| `montar_apendices.py` | Junta os apêndices; monta o G capítulo a capítulo |
| `verificar_livro.py` | Checagens de texto, números, fórmulas, código, siglas, tabelas, figuras, gabaritos e log |
| `amostrar_paginas.py` | Renderiza páginas do PDF para inspeção visual |
| `citar_figuras.py` | Acrescenta citações de figuras que faltam |
| `corrigir_math.py` | Remove espaços junto aos cifrões da matemática inline |
| `gerar_glossario.py` | Glossário consolidado entre marcadores |
| `inserir_apos.py` | Insere texto depois de um bloco de código |

Requisitos: Python 3.11+, pandoc, Tectonic; poppler recomendado. Ver `REQUISITOS.md`.
