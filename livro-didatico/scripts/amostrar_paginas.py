"""Renderiza páginas do PDF em PNG para inspeção visual: capa, sumário, abertura de cada capítulo e de cada
apêndice, e páginas sorteadas (semente fixa). Saída em build/paginas/.

Uso: python3 ferramentas/amostrar_paginas.py [--paginas 5,10-12] [--sorteio 8] [--dpi 70]
"""
import argparse
import random
import re
import subprocess
import sys

from _comum import RAIZ, carregar_config, programa


def faixas(txt):
    out = set()
    for parte in txt.split(","):
        a, _, b = parte.partition("-")
        out |= set(range(int(a), int(b or a) + 1))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paginas", default="")
    ap.add_argument("--sorteio", type=int, default=8)
    ap.add_argument("--dpi", type=int, default=70)
    a = ap.parse_args()
    cfg = carregar_config()
    pdf = RAIZ / "saida" / f"{cfg['saida']}.pdf"
    pdftoppm, pdftotext = programa("pdftoppm"), programa("pdftotext")
    if not pdf.exists():
        sys.exit("PDF não encontrado: rode ferramentas/gerar_livro.py")
    if not (pdftoppm and pdftotext):
        sys.exit("poppler não encontrado (pdftoppm, pdftotext): rode ferramentas/verificar_ambiente.py")

    paginas_txt = subprocess.run([pdftotext, "-layout", str(pdf), "-"], capture_output=True, text=True).stdout.split("\f")
    n = len(paginas_txt) - (1 if not paginas_txt[-1].strip() else 0)
    escolha = {1, 2, 3} | (faixas(a.paginas) if a.paginas else set())
    for i, t in enumerate(paginas_txt[:n], 1):
        topo = " ".join(t.split()[:6])
        if re.search(r"(Capítulo \d+|Apêndice [A-Z])\b", topo) and i > 3:
            escolha.add(i)
    random.seed(20261012)
    resto = [p for p in range(4, n + 1) if p not in escolha]
    escolha |= set(random.sample(resto, min(a.sorteio, len(resto))))

    destino = RAIZ / "build" / "paginas"
    destino.mkdir(parents=True, exist_ok=True)
    for p in sorted(escolha):
        if p <= n:
            subprocess.run([pdftoppm, "-f", str(p), "-l", str(p), "-r", str(a.dpi), "-png", str(pdf), str(destino / "p")], check=True)
    print(f"{len(escolha)} páginas de {n} em build/paginas/: {sorted(escolha)}")
    print("Abra cada imagem e procure: figura cortada ou ausente, tabela estourando a margem, fórmula quebrada, "
          "caixa sem filete, código ilegível, título órfão no pé da página.")


if __name__ == "__main__":
    main()
