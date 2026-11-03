"""Cria um capítulo a partir dos modelos: capNN/ (abertura, seção, laboratório, exercícios e resumo),
os dois arquivos de gabarito do Apêndice G, as pastas de código e figuras, e o registra em livro.toml.
Nunca sobrescreve arquivos existentes.

Uso: python3 ferramentas/novo_capitulo.py N "Título do capítulo"
"""
import re
import sys
from pathlib import Path

from _comum import RAIZ, carregar_config

MODELOS = Path(__file__).resolve().parent / "modelos"

FIG = '''"""Figuras do capítulo {N}. Uma função por figura; rode na raiz do projeto: python codigo/figuras/fig_cap{NN}.py"""
from estilo import plt, COR, chamada, legenda_abaixo, salvar, fmt  # noqa: F401


def fig_{N}_01_exemplo():
    fig, ax = plt.subplots(figsize=(7.5, 4))
    # ax.plot(x, y, color=COR["..."], label="...")
    ax.set_xlabel("Grandeza (unidade)")
    ax.set_ylabel("Grandeza (unidade)")
    legenda_abaixo(ax, ncol=2)
    salvar(fig, "figuras/cap{NN}/f{N}_01_exemplo.png")


if __name__ == "__main__":
    fig_{N}_01_exemplo()
'''


def escreve(alvo, texto, criados):
    if alvo.exists():
        print("  mantido:", alvo.relative_to(RAIZ))
        return
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text(texto, encoding="utf-8")
    criados.append(alvo)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    n = int(sys.argv[1])
    titulo = sys.argv[2]
    nn = f"{n:02d}"
    cap = f"cap{nn}"
    trocas = {"{{N}}": str(n), "{{NN}}": nn, "{{TITULO_CAPITULO}}": titulo}

    def preenche(s):
        for k, v in trocas.items():
            s = s.replace(k, v)
        return s

    criados = []
    for f in sorted((MODELOS / "capitulo").glob("*.md")):
        escreve(RAIZ / cap / f.name, preenche(f.read_text(encoding="utf-8")), criados)
    for f in sorted((MODELOS / "apendice_g").glob("*.md")):
        escreve(RAIZ / "apendices" / f.name.replace("NN", nn), preenche(f.read_text(encoding="utf-8")), criados)
    escreve(RAIZ / "codigo" / "figuras" / f"fig_{cap}.py", FIG.format(N=n, NN=nn), criados)
    (RAIZ / "codigo" / cap).mkdir(parents=True, exist_ok=True)
    (RAIZ / "figuras" / cap).mkdir(parents=True, exist_ok=True)

    cfg = carregar_config()
    caps = cfg["estrutura"]["capitulos"]
    if cap not in caps:
        caps = sorted(caps + [cap])
        toml = (RAIZ / "livro.toml").read_text(encoding="utf-8")
        nova = "capitulos = [" + ", ".join(f'"{c}"' for c in caps) + "]"
        toml, k = re.subn(r"^capitulos\s*=\s*\[.*?\]", nova, toml, count=1, flags=re.S | re.M)
        if k != 1:
            sys.exit("Não achei a linha 'capitulos = [...]' em livro.toml; acrescente o capítulo à mão.")
        (RAIZ / "livro.toml").write_text(toml, encoding="utf-8")
        print(f"livro.toml: {nova}")
    print(f"{cap}: {len(criados)} arquivos criados.")


if __name__ == "__main__":
    main()
