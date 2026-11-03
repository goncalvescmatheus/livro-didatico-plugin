"""Garante que toda figura seja citada no texto: se 'Figura X.Y' não aparece fora da própria legenda,
acrescenta ' (Figura X.Y)' ao fim do parágrafo de texto anterior à figura (ou do seguinte, se o anterior for
título, tabela, fórmula ou código). Revise o resultado: a citação pode ficar num lugar estranho.

Uso: python3 ferramentas/citar_figuras.py capNN/*.md ...   (sem argumentos: todos os capítulos de livro.toml)
"""
import re
import sys

from _comum import RAIZ, capitulo_arquivos, carregar_config

LEGENDA = re.compile(r"^!\[Figura ([0-9A-Z]+\.\d+) —")


def ruim(x):
    return x.startswith(("|", "#", "!", "```", "$$", "\\end", "<!--", ">")) or x.endswith("$$") or not x.strip()


def main():
    arqs = sys.argv[1:] or [str(f) for c in carregar_config()["estrutura"]["capitulos"] for f in capitulo_arquivos(RAIZ, c)]
    textos = {f: open(f, encoding="utf-8").read() for f in arqs}
    corpo = "\n".join(l for t in textos.values() for l in t.split("\n") if not LEGENDA.match(l))

    def citada(num):
        return re.search(rf"Figuras? (?:[0-9A-Z]+\.\d+ (?:e|a) )?{re.escape(num)}(?!\d)", corpo)

    for f, t in textos.items():
        ls, mudou = t.split("\n"), False
        for i, l in enumerate(ls):
            m = LEGENDA.match(l)
            if not m or citada(m.group(1)):
                continue
            j = i - 1
            while j >= 0 and not ls[j].strip():
                j -= 1
            if j < 0 or ruim(ls[j].rstrip()):
                j = i + 1
                while j < len(ls) and ruim(ls[j].rstrip()):
                    j += 1
                if j >= len(ls):
                    print("SEM LUGAR", f, m.group(1))
                    continue
            alvo, ref = ls[j].rstrip(), f" (Figura {m.group(1)})"
            if alvo.endswith((".", ":", ";")):
                alvo = alvo[:-1] + ref + alvo[-1]
            elif alvo.endswith(".**"):
                alvo = alvo[:-3] + "**" + ref + "."
            else:
                alvo += ref
            ls[j], mudou = alvo, True
            corpo += "\n" + alvo
            print(f, m.group(1), "->", alvo[-70:])
        if mudou:
            open(f, "w", encoding="utf-8").write("\n".join(ls))


if __name__ == "__main__":
    main()
