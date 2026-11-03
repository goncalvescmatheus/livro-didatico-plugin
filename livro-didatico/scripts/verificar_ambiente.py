"""Verifica as ferramentas do livro e mostra como instalar o que falta.

Uso:
  python3 verificar_ambiente.py              # só verifica (não instala nada)
  python3 verificar_ambiente.py --instalar   # pergunta item a item, no terminal, antes de instalar
  python3 verificar_ambiente.py --instalar --sim   # instala o que falta sem perguntar:
                                                   # use SÓ depois de o usuário autorizar no chat

Pacotes Python são verificados no interpretador que roda este script; para checar o ambiente
virtual do projeto, rode-o com .venv/bin/python.
"""
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
EXTRA_PATH = ["/opt/homebrew/bin", "/usr/local/bin", os.path.expanduser("~/.cargo/bin")]

# nome: (comando de versão, obrigatória?, para quê, {sistema: comando de instalação})
FERRAMENTAS = {
    "pandoc": (["pandoc", "--version"], True, "Markdown -> LaTeX e DOCX",
               {"mac": "brew install pandoc", "apt": "sudo apt-get install -y pandoc",
                "win": "winget install --id JohnMacFarlane.Pandoc -e"}),
    "tectonic": (["tectonic", "--version"], True, "compilar o PDF (baixa pacotes e fontes na 1ª execução)",
                 {"mac": "brew install tectonic", "apt": "conda install -y -c conda-forge tectonic",
                  "win": "winget install --id TectonicTypesetting.Tectonic -e"}),
    "pdftoppm": (["pdftoppm", "-v"], False, "renderizar páginas do PDF para inspeção (poppler)",
                 {"mac": "brew install poppler", "apt": "sudo apt-get install -y poppler-utils",
                  "win": "winget install --id oschwartz10612.Poppler -e"}),
    "pdfimages": (["pdfimages", "-v"], False, "contar figuras no PDF (poppler)",
                  {"mac": "brew install poppler", "apt": "sudo apt-get install -y poppler-utils",
                   "win": "winget install --id oschwartz10612.Poppler -e"}),
    "git": (["git", "--version"], False, "versionar o projeto",
            {"mac": "brew install git", "apt": "sudo apt-get install -y git", "win": "winget install --id Git.Git -e"}),
}


def sistema():
    s = platform.system()
    if s == "Darwin":
        return "mac"
    if s == "Windows":
        return "win"
    return "apt" if shutil.which("apt-get") else "outro"


def achar(nome):
    p = shutil.which(nome)
    if p:
        return p
    for d in EXTRA_PATH:
        c = Path(d) / nome
        if c.exists():
            return str(c)
    return None


def versao(cmd):
    exe = achar(cmd[0])
    if not exe:
        return None
    try:
        r = subprocess.run([exe] + cmd[1:], capture_output=True, text=True, timeout=30)
        linha = (r.stdout or r.stderr).strip().splitlines()
        return linha[0] if linha else "ok"
    except Exception as e:  # executável quebrado
        return f"erro: {e}"


def python_novo():
    """Um Python 3.11+ já instalado (o atual, o do Homebrew ou python3.1x no PATH), ou None."""
    if sys.version_info >= (3, 11):
        return sys.executable
    for nome in ("python3.14", "python3.13", "python3.12", "python3.11", "python3"):
        exe = achar(nome)
        cands = [exe] + [str(Path(d) / nome) for d in EXTRA_PATH]
        for c in cands:
            if c and Path(c).exists():
                r = subprocess.run([c, "-c", "import sys; print(sys.version_info >= (3, 11))"], capture_output=True, text=True)
                if r.stdout.strip() == "True":
                    return c
    return None


def pacotes_python():
    req = RAIZ / "requirements.txt"  # raiz do projeto ou do plugin
    if not req.exists():
        return [], None
    try:
        from importlib.metadata import version, PackageNotFoundError
    except ImportError:
        return [], req
    faltam = []
    for linha in req.read_text(encoding="utf-8").splitlines():
        linha = linha.split("#")[0].strip()
        if not linha:
            continue
        nome = re.split(r"[<>=!~\[ ]", linha)[0]
        try:
            version(nome)
        except PackageNotFoundError:
            faltam.append(linha)
    return faltam, req


def main():
    instalar = "--instalar" in sys.argv
    sim = "--sim" in sys.argv
    so = sistema()
    pend = []  # (descrição, comando)

    print(f"Sistema: {platform.system()} ({so})")
    py = python_novo()
    if py == sys.executable:
        print(f"[ok] Python {platform.python_version()} ({py})")
    elif py:
        print(f"[ok] Python 3.11+ em {py} (este script rodou com {platform.python_version()}; use aquele)")
    else:
        print(f"[FALTA] Python 3.11+ (este é {platform.python_version()})")
        cmd = {"mac": "brew install python", "apt": "sudo apt-get install -y python3 python3-venv",
               "win": "winget install --id Python.Python.3.12 -e"}.get(so)
        pend.append(("Python 3.11+", cmd))

    for nome, (cmd, obrig, uso, inst) in FERRAMENTAS.items():
        v = versao(cmd)
        marca = "ok" if v else ("FALTA" if obrig else "falta (opcional)")
        print(f"[{marca}] {nome}: {v or '-'}  ({uso})")
        if not v:
            c = inst.get(so)
            if c and not any(c == p[1] for p in pend):
                pend.append((nome, c))
            elif not c:
                print(f"      instale {nome} pelo site oficial (sistema não reconhecido)")

    faltam, req = pacotes_python()
    if req:
        if faltam:
            print(f"[FALTA] pacotes Python em {sys.executable}: {', '.join(faltam)}")
            if (RAIZ / "livro.toml").exists():  # dentro de um projeto: ambiente virtual do projeto
                venv = RAIZ / ".venv"
                pip = venv / ("Scripts/pip.exe" if so == "win" else "bin/pip")
                cria = "" if venv.exists() else f"{py or 'python3'} -m venv {venv} && "
                pend.append(("pacotes Python (requirements.txt)", f"{cria}{pip} install -r {req}"))
            else:
                print("      (instale-os no ambiente virtual de cada livro, depois de criar o projeto)")
        else:
            print(f"[ok] pacotes Python de {req.name}")

    if not pend:
        print("\nTudo pronto.")
        return 0

    print("\nPara instalar o que falta:")
    for d, c in pend:
        print(f"  - {d}: {c}")
    if not instalar:
        print("\nNada foi instalado. Peça permissão ao usuário antes de rodar estes comandos.")
        return 1

    interativo = sys.stdin.isatty()
    if not sim and not interativo:
        print("\nSem --sim e sem terminal interativo: nada foi instalado.")
        return 1
    for d, c in pend:
        if not sim:
            r = input(f"Instalar {d} com '{c}'? [s/N] ").strip().lower()
            if r not in ("s", "sim", "y", "yes"):
                print("  pulado")
                continue
        print(f"$ {c}")
        subprocess.run(c, shell=True)
    print("\nVerifique de novo: python3 verificar_ambiente.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
