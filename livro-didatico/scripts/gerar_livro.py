"""Gera o livro completo a partir da fonte única em Markdown:
PDF via LaTeX (pandoc + Tectonic) e Word (pandoc). Saídas em saida/, intermediários em build/.

Uso: python3 ferramentas/gerar_livro.py [--sem-pdf] [--sem-docx]
"""
import json
import shutil
import subprocess
import sys

from _comum import RAIZ, capitulo_arquivos, carregar_config, programa
from montar_apendices import montar


def metadados(cfg):
    campos = {"title": cfg["titulo"], "subtitle": cfg["subtitulo"], "author": cfg["autor"],
              "date": cfg["data"], "lang": cfg["idioma"]}
    linhas = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in campos.items() if v] + ["---", ""]
    return "\n".join(linhas)


def fonte_unica(cfg):
    partes = [metadados(cfg)]
    for nome in cfg["estrutura"]["pre_textuais"]:
        arq = RAIZ / nome
        if arq.exists():
            partes.append(arq.read_text(encoding="utf-8"))
    for cap in cfg["estrutura"]["capitulos"]:
        arqs = capitulo_arquivos(RAIZ, cap)
        if not arqs:
            print(f"aviso: {cap}/ sem arquivos .md", file=sys.stderr)
        partes.extend(a.read_text(encoding="utf-8") for a in arqs)
    partes.append(montar(RAIZ, cfg))
    return "\n\n".join(partes) + "\n"


def roda(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print(r.stdout[-3000:], r.stderr[-3000:], sep="\n", file=sys.stderr)
        sys.exit(f"falhou: {' '.join(map(str, cmd[:3]))} …")
    return r


def main():
    cfg = carregar_config()
    pandoc = programa("pandoc")
    if not pandoc:
        sys.exit("pandoc não encontrado. Rode python3 ferramentas/verificar_ambiente.py e peça permissão para instalar.")
    build, saida = RAIZ / "build", RAIZ / "saida"
    build.mkdir(exist_ok=True)
    saida.mkdir(exist_ok=True)
    md = build / "livro.md"
    md.write_text(fonte_unica(cfg), encoding="utf-8")
    nome = cfg["saida"]
    lang = cfg["idioma"]

    if "--sem-pdf" not in sys.argv:
        tectonic = programa("tectonic")
        if not tectonic:
            sys.exit("tectonic não encontrado. Rode python3 ferramentas/verificar_ambiente.py e peça permissão para instalar.")
        tex = build / "livro.tex"
        roda([pandoc, str(md), "-s", "-o", str(tex), "--from", "markdown", "--to", "latex",
              "--top-level-division=chapter", "--toc", "--toc-depth=1",
              "--lua-filter", str(RAIZ / "latex" / "filtro.lua"),
              "--include-in-header", str(RAIZ / "latex" / "cabecalho.tex"),
              "--resource-path", str(RAIZ),
              "-V", "documentclass=book", "-V", "classoption=openany", "-V", f"lang={lang}", "-V", "fontsize=11pt",
              "-V", "colorlinks=true", "-V", "linkcolor=azul", "-V", "urlcolor=azul"])
        # o .tex fica em build/: as figuras são referidas a partir da raiz
        tex.write_text(tex.read_text(encoding="utf-8").replace("{figuras/", "{../figuras/"), encoding="utf-8")
        r = subprocess.run([tectonic, "-X", "compile", "--keep-logs", "livro.tex"], cwd=build, capture_output=True, text=True)
        (build / "tectonic.log").write_text(r.stdout + r.stderr, encoding="utf-8")
        if r.returncode != 0:
            print("\n".join((r.stdout + r.stderr).splitlines()[-40:]), file=sys.stderr)
            sys.exit("Tectonic falhou; veja build/tectonic.log e build/livro.log.")
        shutil.copy2(build / "livro.pdf", saida / f"{nome}.pdf")
        print(f"gerado: saida/{nome}.pdf")

    if "--sem-docx" not in sys.argv:
        ref = RAIZ / "latex" / "referencia.docx"
        cmd = [pandoc, str(md), "-o", str(saida / f"{nome}.docx"), "--top-level-division=chapter", "--toc",
               "--toc-depth=2", "--resource-path", str(RAIZ), "-M", f"lang={lang}"]
        if ref.exists():  # estilos opcionais do Word
            cmd += ["--reference-doc", str(ref)]
        roda(cmd)
        print(f"gerado: saida/{nome}.docx")
    print("Agora: python3 ferramentas/verificar_livro.py")


if __name__ == "__main__":
    main()
