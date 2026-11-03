# Requisitos

Tudo é gratuito e de código aberto. `scripts/verificar_ambiente.py` (no projeto: `ferramentas/verificar_ambiente.py`) diz o que está faltando e o comando para instalar.

## Regra de permissão

**Nada é baixado ou instalado sem permissão explícita do usuário.** O fluxo é:

1. Rodar `python3 ferramentas/verificar_ambiente.py` (só verifica, não instala).
2. Mostrar ao usuário, no chat, o que falta, de onde viria e o comando exato.
3. Esperar um "sim" claro. Sem resposta, não instalar.
4. Instalar com o comando mostrado, ou com `python3 ferramentas/verificar_ambiente.py --instalar --sim` (que roda só os comandos listados). Em terminal interativo, `--instalar` sem `--sim` pergunta item a item.
5. Rodar a verificação de novo e informar o resultado.

## Ferramentas do sistema

| Ferramenta | Obrigatória? | Para quê | macOS (Homebrew) | Debian/Ubuntu | Windows (winget) |
| --- | --- | --- | --- | --- | --- |
| Python 3.11+ | Sim | Scripts do livro (usa `tomllib`) | `brew install python` | `sudo apt install python3 python3-venv` | `winget install Python.Python.3.12` |
| pandoc 3+ | Sim | Markdown → LaTeX e DOCX | `brew install pandoc` | `sudo apt install pandoc` (ou o `.deb` do site, se a versão for antiga) | `winget install JohnMacFarlane.Pandoc` |
| Tectonic | Sim, para PDF | Compila o LaTeX; baixa pacotes e fontes na primeira execução | `brew install tectonic` | `conda install -c conda-forge tectonic` ou o instalador oficial | `winget install TectonicTypesetting.Tectonic` |
| poppler | Recomendada | Inspeção do PDF (`pdftoppm`, `pdfinfo`, `pdfimages`, `pdftotext`) | `brew install poppler` | `sudo apt install poppler-utils` | `winget install oschwartz10612.Poppler` |
| git | Recomendada | Versionar o projeto | `brew install git` | `sudo apt install git` | `winget install Git.Git` |

Os identificadores do `winget` e os pacotes das distribuições mudam com o tempo; confira com `winget search <nome>` ou `apt-cache policy <nome>` antes de propor o comando ao usuário.

O Tectonic baixa pacotes LaTeX e fontes (Libertinus, DejaVu) na **primeira** compilação, o que exige internet uma vez e também deve ser avisado ao usuário.

## Pacotes Python

Em ambiente virtual do projeto:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt     # Windows: .venv\Scripts\pip install -r requirements.txt
```

`requirements.txt` traz o núcleo (cálculo, dados, figuras). Pacotes específicos do assunto do livro (otimização, estatística avançada, modelos da área) são acrescentados no início do projeto, preferindo os abertos, e registrados na memória do projeto.
