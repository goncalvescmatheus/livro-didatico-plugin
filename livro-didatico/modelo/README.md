# {{TITULO}}

{{SUBTITULO}}

## Estrutura

| Pasta ou arquivo | Conteúdo |
| --- | --- |
| `CLAUDE.md` | Regras do projeto para o assistente |
| `FICHA_DO_LIVRO.md`, `PLANO_DE_ESCRITA.md` | Quem é o leitor e o que o livro cobre |
| `MEMORIA_DO_PROJETO.md` | Estado, decisões, números-chave, pendências |
| `ANOTACOES_CORRECAO.md` | Correções pendentes da leitura do autor |
| `livro.toml` | Título, idioma, separadores, capítulos e apêndices |
| `0p-prefacio.md`, `0s-siglas.md` | Prefácio e lista de siglas |
| `capNN/` | Um capítulo por pasta; arquivos concatenados em ordem alfabética |
| `apendices/` | Apêndices A a H; o G é montado de `G-solucoes-capNN.md` e `G-recuperacao-capNN.md` |
| `figuras/capNN/` | Imagens geradas pelo código |
| `codigo/` | Scripts que produzem cada número, tabela e figura (`codigo/figuras/estilo.py`) |
| `dados/` | Dados brutos e processados; `dados/FONTES.md` com origem e licença |
| `latex/` | Preâmbulo e filtro do PDF |
| `guia/` | Guias de pedagogia, escrita, reprodutibilidade, figuras e produção |
| `ferramentas/` | Scripts de criação, geração e verificação |
| `build/`, `saida/` | Intermediários e o livro final (PDF e DOCX) |

## Como gerar

```bash
python3 ferramentas/verificar_ambiente.py      # o que falta instalar (não instala nada)
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 ferramentas/gerar_livro.py             # saida/livro.pdf e saida/livro.docx
python3 ferramentas/verificar_livro.py         # checagens
python3 ferramentas/amostrar_paginas.py        # páginas para inspeção visual
```
