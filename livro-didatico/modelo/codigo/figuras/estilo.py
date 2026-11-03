"""Estilo comum das figuras do livro.

Princípios didáticos (ver guia/FIGURAS.md):
- nenhum texto sobre curvas: legendas abaixo do gráfico (legenda_abaixo);
- pontos citados no texto com linhas de chamada tracejadas até os eixos e o valor exato (chamada);
- números no padrão do idioma do livro (fmt), também nos eixos;
- cores fixas por conceito (COR) em todos os capítulos;
- largura máxima LMAX polegadas, para que o texto impresso não fique abaixo de ~7 pt.

Rode os scripts de figura a partir da raiz do projeto (os caminhos de saída são relativos a ela).
"""
import locale
import warnings
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter, ScalarFormatter

try:
    import tomllib
    _cfg = tomllib.loads((Path(__file__).resolve().parents[2] / "livro.toml").read_text(encoding="utf-8"))
except Exception:  # sem livro.toml ou Python < 3.11: padrão português
    _cfg = {}
DECIMAL = _cfg.get("numeros", {}).get("decimal", ",")
MILHAR = _cfg.get("numeros", {}).get("milhar", ".")
try:  # meses e dias no idioma do livro nos eixos de datas
    locale.setlocale(locale.LC_TIME, _cfg.get("idioma", "pt-BR").replace("-", "_") + ".UTF-8")
except locale.Error:
    pass

AZUL, LARANJA, VERDE, VERMELHO, ROXO, CINZA, AMARELO = "#1f5f99", "#e07b24", "#2e8b57", "#c0392b", "#7d3c98", "#7f8c8d", "#d4ac0d"
CORES = [AZUL, LARANJA, VERDE, VERMELHO, ROXO, CINZA, AMARELO, "#16a085"]

# Cores semânticas: o mesmo conceito tem a mesma cor em todo o livro. Preencha no início do projeto.
COR = {
    "referencia": "#222222",   # média, linha de base, valor de referência
    "cenario_base": AZUL,
    "cenario_alto": VERMELHO,
    "cenario_baixo": VERDE,
    "incerteza": "#8fb3d9",    # faixas e intervalos
    # "conceito_a": AMARELO, "conceito_b": ROXO, ...
}
# Cores por ano, para séries históricas comparadas.
ANO = {}

LMAX = 8.5  # largura máxima (polegadas)

plt.rcParams.update({
    "figure.dpi": 110, "savefig.dpi": 220, "savefig.bbox": "tight", "savefig.pad_inches": 0.04,
    "font.size": 10.5, "axes.titlesize": 11, "axes.titleweight": "bold", "axes.labelsize": 10.5,
    "xtick.labelsize": 9.5, "ytick.labelsize": 9.5, "legend.fontsize": 9.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": False, "legend.frameon": False, "axes.unicode_minus": True,
    "axes.prop_cycle": matplotlib.cycler(color=CORES),
    "axes.titlepad": 10, "lines.linewidth": 2,
})

_subplots, _figure = plt.subplots, plt.figure


def _limita(kw):
    fs = kw.get("figsize")
    if fs and fs[0] > LMAX:
        s = LMAX / fs[0]
        kw["figsize"] = (fs[0] * s, fs[1] * s)
    return kw


plt.subplots = lambda *a, **kw: _subplots(*a, **_limita(kw))
plt.figure = lambda *a, **kw: _figure(*a, **_limita(kw))


def fmt(x, nd=0):
    """Formata número no padrão do livro (português: 1.234,5), com o sinal de menos tipográfico."""
    s = f"{x:,.{nd}f}".replace(",", "\0").replace(".", DECIMAL).replace("\0", MILHAR)
    if s.startswith("-"):
        s = "−" + s[1:]
        if set(s[1:]) <= set("0" + DECIMAL + MILHAR):
            s = s[1:]  # "−0" vira "0"
    return s


br = fmt  # nome curto antigo


def _decimais(locs):
    for nd in range(0, 5):
        if np.all(np.abs(np.asarray(locs) * 10 ** nd - np.round(np.asarray(locs) * 10 ** nd)) < 1e-6):
            return nd
    return 4


def _formata_eixos(fig):
    """Troca os formatadores numéricos padrão por fmt(): separadores do idioma e menos tipográfico."""
    fig.canvas.draw()
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            f = axis.get_major_formatter()
            if type(f) is not ScalarFormatter or axis.get_scale() != "linear":
                continue
            lo, hi = axis.get_view_interval()
            locs = [v for v in axis.get_majorticklocs() if min(lo, hi) - 1e-9 <= v <= max(lo, hi) + 1e-9]
            if not locs or f.get_offset():
                continue  # notação científica: mantém o padrão
            maior = max(abs(v) for v in locs)
            if 0 < maior < 1e-3:
                continue
            nd = _decimais(locs)
            milhar = maior >= 10000
            axis.set_major_formatter(FuncFormatter(
                lambda v, p, nd=nd, m=milhar: fmt(v, nd) if m else fmt(v, nd).replace(MILHAR, "")))


def _verifica(fig, caminho):
    """Avisos de qualidade: texto com '_' ou '^' cru e caixas de texto sobre curvas."""
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    for t in fig.findobj(matplotlib.text.Text):
        s = t.get_text()
        if s and "$" not in s and ("_" in s or "^" in s) and t.get_visible():
            warnings.warn(f"{caminho}: texto com símbolo cru: {s[:50]!r}")
    for ax in fig.axes:
        linhas = [l for l in ax.lines if l.get_visible() and len(l.get_xdata()) > 1
                  and not (l.get_linestyle() in ("--", ":") and l.get_linewidth() < 1.2)]
        for t in ax.texts:
            if not t.get_visible() or not t.get_text().strip() or t.get_bbox_patch() is None:
                continue
            bb = t.get_bbox_patch().get_window_extent(r)
            for l in linhas:
                xy = l.get_xydata()
                k = np.linspace(0, len(xy) - 1, 20 * len(xy))
                pts = l.get_transform().transform(np.c_[np.interp(k, np.arange(len(xy)), xy[:, 0]),
                                                        np.interp(k, np.arange(len(xy)), xy[:, 1])])
                dentro = (pts[:, 0] > bb.x0 + 2) & (pts[:, 0] < bb.x1 - 2) & (pts[:, 1] > bb.y0 + 2) & (pts[:, 1] < bb.y1 - 2)
                if dentro.any():
                    warnings.warn(f"{caminho}: caixa sobre curva: {t.get_text()[:40]!r}")
                    break


def salvar(fig, caminho):
    Path(caminho).parent.mkdir(parents=True, exist_ok=True)
    _formata_eixos(fig)
    _verifica(fig, caminho)
    fig.savefig(caminho)
    plt.close(fig)
    print("ok", caminho)


def chamada(ax, x, y, texto=None, cor="#333333", dx=20, dy=20, xlinha=True, ylinha=True, ms=5, fs=9,
            xtxt=None, ytxt=None, pos=None):
    """Marca o ponto (x, y), traça linhas tracejadas até os eixos e escreve o valor numa caixa deslocada.

    dx, dy: deslocamento do rótulo em pontos tipográficos (positivo = direita/acima).
    xtxt/ytxt: textos opcionais junto aos eixos (por exemplo, o valor de x).
    pos: (x, y) em coordenadas de dados para o rótulo; se dado, substitui dx/dy.
    """
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    if xlinha:
        ax.plot([x, x], [y0, y], ls="--", lw=0.9, color=cor, alpha=0.8, zorder=4)
    if ylinha:
        ax.plot([x0, x], [y, y], ls="--", lw=0.9, color=cor, alpha=0.8, zorder=4)
    ax.plot([x], [y], "o", ms=ms, color=cor, zorder=5)
    if texto:
        kw = dict(xytext=pos, textcoords="data", ha="left", va="center") if pos else \
            dict(xytext=(dx, dy), textcoords="offset points", ha="left" if dx >= 0 else "right",
                 va="bottom" if dy >= 0 else "top")
        ax.annotate(texto, (x, y), fontsize=fs, color=cor, **kw,
                    bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=cor, lw=0.6, alpha=0.95),
                    arrowprops=dict(arrowstyle="-", color=cor, lw=0.7), zorder=6)
    caixa = dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9)
    if xtxt:
        ax.annotate(xtxt, (x, y0), xytext=(3, 3), textcoords="offset points", ha="left", va="bottom",
                    fontsize=8.5, color=cor, bbox=caixa, zorder=6)
    if ytxt:
        ax.annotate(ytxt, (x0, y), xytext=(3, 2), textcoords="offset points", ha="left", va="bottom",
                    fontsize=8.5, color=cor, bbox=caixa, zorder=6)
    ax.set_xlim(x0, x1)
    ax.set_ylim(y0, y1)


def legenda_abaixo(alvo, ncol=3, dy=-0.18, handles=None, labels=None, fs=9.5):
    """Coloca a legenda abaixo da área do gráfico (eixo) ou da figura, para não cobrir curvas."""
    if handles is None:
        handles, labels = alvo.get_legend_handles_labels()
    if hasattr(alvo, "transAxes"):
        alvo.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, dy), ncol=ncol, fontsize=fs)
    else:
        alvo.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, dy), ncol=ncol, fontsize=fs)


if __name__ == "__main__":
    assert fmt(1234.5, 1) == "1.234,5" or DECIMAL != ","
    assert fmt(-0.0, 1) == "0,0" or DECIMAL != ","
    print("estilo ok")
