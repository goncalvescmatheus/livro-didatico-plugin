"""Funções comuns às ferramentas do livro: raiz do projeto, configuração (livro.toml) e localização de programas."""
import os
import shutil
import sys
from pathlib import Path

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    try:
        import tomli as tomllib
    except ModuleNotFoundError:
        sys.exit("Python 3.11+ é necessário (ou o pacote 'tomli'). Rode ferramentas/verificar_ambiente.py.")

# As ferramentas ficam em <projeto>/ferramentas/; a raiz é a pasta acima.
RAIZ = Path(__file__).resolve().parent.parent

PADRAO = {
    "titulo": "", "subtitulo": "", "autor": "", "data": "", "idioma": "pt-BR", "saida": "livro",
    "numeros": {"decimal": ",", "milhar": "."},
    "estrutura": {"pre_textuais": ["0p-prefacio.md", "0s-siglas.md"], "capitulos": [],
                  "apendices": ["A", "B", "C", "D", "E", "F", "G", "H"]},
    "verificacao": {
        "caixa_codigo": "Lendo o código",
        "caixas_formula": ["Lendo a fórmula", "Lendo a notação"],
        "linguagens_sem_caixa": ["text"],
        "max_siglas_paragrafo": 3,
        "min_usos_sigla": 3,
        "max_celula": 120,
        # tabelas de referência cujo título já diz o que mostram (não exigem texto antes)
        "titulos_tabela_livre": ["Objetivos", "Notação", "Fórmulas-chave", "Glossário", "Leituras", "Convenções",
                                 "Caixas", "Siglas"],
        "hbox_tolerancia_pt": 20,
        "referencias_internas": ["codigo/cap", "codigo/figuras", "ferramentas/", "build/", "saida/", "guia/",
                                 "apendices/", "MEMORIA_DO_PROJETO", "PLANO_DE_ESCRITA", "ANOTACOES_CORRECAO",
                                 "FICHA_DO_LIVRO", "livro.toml", "verificar_livro", "gerar_livro"],
        "siglas_ignoradas": [],
        "vazamentos_extra": [],
    },
}


def _mescla(base, novo):
    out = dict(base)
    for k, v in novo.items():
        out[k] = _mescla(base[k], v) if isinstance(v, dict) and isinstance(base.get(k), dict) else v
    return out


def carregar_config(raiz=RAIZ):
    arq = Path(raiz) / "livro.toml"
    if not arq.exists():
        sys.exit(f"Não achei {arq}. Rode a ferramenta dentro de um projeto criado por novo_livro.py.")
    with open(arq, "rb") as f:
        return _mescla(PADRAO, tomllib.load(f))


def programa(nome):
    """Caminho do executável, procurando também nas pastas usuais do Homebrew."""
    achado = shutil.which(nome)
    if achado:
        return achado
    for pasta in ("/opt/homebrew/bin", "/usr/local/bin", os.path.expanduser("~/.cargo/bin")):
        p = Path(pasta) / nome
        if p.exists():
            return str(p)
    return None


def capitulo_arquivos(raiz, cap):
    return sorted((Path(raiz) / cap).glob("*.md"))
