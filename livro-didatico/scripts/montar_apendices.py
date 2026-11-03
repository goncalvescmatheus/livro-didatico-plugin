"""Monta os apêndices do livro na ordem de livro.toml. Cada apêndice vira um capítulo do livro.
O Apêndice G é montado capítulo a capítulo a partir de apendices/G-solucoes-capNN.md e
apendices/G-recuperacao-capNN.md (a primeira linha de cada arquivo, o título, é descartada).

Uso como módulo (gerar_livro.py) ou: python3 ferramentas/montar_apendices.py > build/apendices.md
"""
import re
import sys
from pathlib import Path

from _comum import RAIZ, carregar_config

INTRO_G = ("> Soluções completas dos exercícios de nível A, números de referência do nível B, roteiros do nível C "
           "e as respostas comentadas, passo a passo, das perguntas de recuperação, capítulo a capítulo.")


def rebaixa(txt, n=1):
    """Acrescenta n níveis a cada título Markdown, fora de blocos de código."""
    out, codigo = [], False
    for linha in txt.split("\n"):
        if linha.startswith("```"):
            codigo = not codigo
        if n and not codigo and re.match(r"^#{1,5} ", linha):
            linha = "#" * n + linha
        out.append(linha)
    return "\n".join(out)


def sem_titulo(txt):
    return txt.split("\n", 1)[1] if "\n" in txt else ""


def titulo_capitulo(raiz, cap):
    abertura = sorted((raiz / cap).glob("*.md"))
    if abertura:
        m = re.search(r"^# (.+)$", abertura[0].read_text(encoding="utf-8"), re.M)
        if m:
            return m.group(1).strip()
    return f"Capítulo {int(cap[3:])}"


def apendice_g(raiz, caps):
    partes = ["# Apêndice G — Soluções e respostas", "", INTRO_G, ""]
    for cap in caps:
        sol = raiz / "apendices" / f"G-solucoes-{cap}.md"
        rec = raiz / "apendices" / f"G-recuperacao-{cap}.md"
        blocos = [rebaixa(sem_titulo(f.read_text(encoding="utf-8")), 1) for f in (sol, rec) if f.exists()]
        if blocos:
            partes.append(f"## {titulo_capitulo(raiz, cap)}\n")
            partes.extend(blocos)
    return "\n\n".join(partes)


def montar(raiz=RAIZ, cfg=None):
    cfg = cfg or carregar_config(raiz)
    raiz = Path(raiz)
    partes = []
    for letra in cfg["estrutura"]["apendices"]:
        if letra == "G":
            partes.append(apendice_g(raiz, cfg["estrutura"]["capitulos"]))
            continue
        achados = sorted((raiz / "apendices").glob(f"{letra}-*.md"))
        if achados:
            partes.append(achados[0].read_text(encoding="utf-8"))
        else:
            print(f"aviso: apêndice {letra} não encontrado em apendices/", file=sys.stderr)
    return "\n\n".join(partes)


if __name__ == "__main__":
    sys.stdout.write(montar())
