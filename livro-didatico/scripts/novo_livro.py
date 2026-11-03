"""Cria um projeto de livro a partir do plugin: estrutura, regras (CLAUDE.md), guias, ferramentas e modelos.
Nunca sobrescreve arquivos existentes.

Uso: python3 novo_livro.py DESTINO --titulo "..." [--subtitulo "..."] [--autor "..."] [--data "Março de 2027"] [--idioma pt-BR]
"""
import argparse
import shutil
import sys
from pathlib import Path

PLUGIN = Path(__file__).resolve().parent.parent
TEXTO = {".md", ".toml", ".tex", ".lua", ".py", ".txt", ".gitignore", ""}


def copiar(origem, destino, trocas, criados, pulados):
    for f in sorted(origem.rglob("*")):
        if f.is_dir() or "__pycache__" in f.parts:
            continue
        alvo = destino / f.relative_to(origem)
        if alvo.exists():
            pulados.append(alvo)
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        if f.suffix in TEXTO or f.name == ".gitignore":
            s = f.read_text(encoding="utf-8")
            for k, v in trocas.items():
                s = s.replace(k, v)
            alvo.write_text(s, encoding="utf-8")
        else:
            shutil.copy2(f, alvo)
        criados.append(alvo)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("destino")
    ap.add_argument("--titulo", required=True)
    ap.add_argument("--subtitulo", default="")
    ap.add_argument("--autor", default="")
    ap.add_argument("--data", default="")
    ap.add_argument("--idioma", default="pt-BR")
    a = ap.parse_args()

    dest = Path(a.destino).expanduser().resolve()
    dest.mkdir(parents=True, exist_ok=True)
    trocas = {"{{TITULO}}": a.titulo, "{{SUBTITULO}}": a.subtitulo, "{{AUTOR}}": a.autor,
              "{{DATA}}": a.data, "{{IDIOMA}}": a.idioma}
    criados, pulados = [], []
    copiar(PLUGIN / "modelo", dest, trocas, criados, pulados)
    copiar(PLUGIN / "guia", dest / "guia", {}, criados, pulados)
    copiar(PLUGIN / "scripts", dest / "ferramentas", {}, criados, pulados)
    copiar(PLUGIN / "modelo_capitulo", dest / "ferramentas" / "modelos" / "capitulo", {}, criados, pulados)
    copiar(PLUGIN / "modelo_apendice_g", dest / "ferramentas" / "modelos" / "apendice_g", {}, criados, pulados)
    for nome in ("CLAUDE.md", "REQUISITOS.md", "requirements.txt"):
        alvo = dest / nome
        if alvo.exists():
            pulados.append(alvo)
        else:
            shutil.copy2(PLUGIN / nome, alvo)
            criados.append(alvo)
    for d in ("figuras", "codigo/figuras", "dados/brutos", "dados/processados", "build", "saida"):
        (dest / d).mkdir(parents=True, exist_ok=True)

    print(f"Projeto em {dest}: {len(criados)} arquivos criados, {len(pulados)} já existiam (mantidos).")
    for p in pulados:
        print("  mantido:", p.relative_to(dest))
    print("Próximos passos: preencher FICHA_DO_LIVRO.md e PLANO_DE_ESCRITA.md; "
          "python3 ferramentas/verificar_ambiente.py; python3 ferramentas/novo_capitulo.py 0 \"Fundamentos\".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
