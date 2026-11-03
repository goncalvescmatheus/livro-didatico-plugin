"""Verifica o livro: texto (vazamentos, referências internas, marcadores), contas e números, siglas,
tabelas, fórmulas, código, figuras, gabaritos e o log do LaTeX. As regras estão em guia/ESCRITA.md.

ERRO: precisa ser corrigido.  AVISO: revise; pode ser legítimo.
Uso: python3 ferramentas/verificar_livro.py [--grupo NOME ...] [--max N]
Sai com código 1 se houver ERRO.
"""
import argparse
import collections
import re
import subprocess
import sys
from pathlib import Path

from _comum import RAIZ, capitulo_arquivos, carregar_config, programa

# Vazamentos de processo: ERRO (quase sempre indevidos) e AVISO (podem ser legítimos no contexto).
VAZAMENTOS = [
    r"\bcorrigimos\b", r"\berramos\b", r"\bleitura antiga\b", r"interpretação crítica do que fizemos",
    r"\bnesta sessão\b", r"\bcomo (discutimos|combinamos)\b", r"\bconforme solicitado\b", r"\bo autor pediu\b",
    r"\bvou (calcular|mostrar|agora|fazer)\b", r"\bo modelo errou porque\b", r"\bscratchpad\b",
    r"\(verificar\)", r"\bTODO\b", r"\bFIXME\b", r"\bXXX\b", r"\bplaceholder\b",
]
VAZAMENTOS_FRACOS = [r"\bna conversa\b", r"\bversão (anterior|antiga)\b", r"\bcorrigid[oa]s?\b", r"\ba confirmar\b",
                     r"\bcomo pedido\b"]
UNIDADES = {"MW", "GW", "TW", "KW", "MWH", "GWH", "TWH", "KWH", "MVA", "MVAR", "MVARH", "PJ", "EJ", "CO2", "NOX",
            "SO2", "PDF", "DOCX", "HTML", "URL", "API", "CSV", "JSON", "UTC", "CET", "CEST", "OK"}
SIGLA = re.compile(r"\b[A-Z][A-Z0-9]*[A-Z0-9]\b")
ROMANO = re.compile(r"^[IVXLCDM]+$")


class Relatorio:
    def __init__(self, maximo):
        self.itens = collections.defaultdict(list)
        self.maximo = maximo

    def add(self, grupo, nivel, onde, msg):
        self.itens[grupo].append((nivel, onde, msg))

    def imprime(self, grupos=None):
        erros = avisos = 0
        for g, lst in self.itens.items():
            if grupos and g not in grupos:
                continue
            e = sum(1 for n, *_ in lst if n == "ERRO")
            erros += e
            avisos += len(lst) - e
            print(f"\n== {g}: {e} erro(s), {len(lst) - e} aviso(s)")
            for n, onde, msg in lst[: self.maximo]:
                print(f"  {n:5} {onde}: {msg}")
            if len(lst) > self.maximo:
                print(f"  … mais {len(lst) - self.maximo}")
        print(f"\nTotal: {erros} erro(s), {avisos} aviso(s).")
        return erros


def limpa_inline(linha):
    """Remove código inline, matemática inline, URLs e caminhos de imagem de uma linha de texto."""
    linha = re.sub(r"`[^`]*`", " ", linha)
    linha = re.sub(r"(?<!\\)\$[^$]+(?<!\\)\$", " ", linha)
    linha = re.sub(r"\]\([^)]*\)", "]", linha)
    linha = re.sub(r"\b(US|R|A|C|NZ)\\?\$", " ", linha)  # moedas não são siglas
    return re.sub(r"https?://\S+", " ", linha)


def linhas_texto(texto):
    """(número da linha, linha, dentro_de_codigo, dentro_de_formula_destacada)."""
    codigo = formula = False
    for i, l in enumerate(texto.split("\n"), 1):
        if l.lstrip().startswith("```") and not formula:
            yield i, l, True, False
            codigo = not codigo
            continue
        if not codigo and formula:
            yield i, l, False, True
            formula = "$$" not in l  # a linha que contém o $$ de fechamento encerra a fórmula
            continue
        if not codigo and l.strip().startswith("$$"):
            yield i, l, False, True
            formula = l.strip().count("$$") == 1  # "$$" sozinho abre um bloco de várias linhas
            continue
        yield i, l, codigo, False


def arquivos_livro(cfg):
    lst = [RAIZ / f for f in cfg["estrutura"]["pre_textuais"] if (RAIZ / f).exists()]
    for cap in cfg["estrutura"]["capitulos"]:
        lst += capitulo_arquivos(RAIZ, cap)
    lst += sorted((RAIZ / "apendices").glob("*.md"))
    return lst


def rel(p):
    return str(Path(p).relative_to(RAIZ))


# ---------------------------------------------------------------- texto
def checa_texto(arqs, cfg, R):
    comp = lambda lst: [re.compile(p, re.I if p.islower() else 0) for p in lst]
    vaz = [(p, "ERRO") for p in comp(VAZAMENTOS + cfg["verificacao"]["vazamentos_extra"])]
    vaz += [(p, "AVISO") for p in comp(VAZAMENTOS_FRACOS)]
    internas = cfg["verificacao"]["referencias_internas"]
    for a in arqs:
        for i, l, cod, _ in linhas_texto(a.read_text(encoding="utf-8")):
            onde = f"{rel(a)}:{i}"
            if "{{" in l and "}}" in l:
                R.add("texto", "ERRO", onde, f"marcador não preenchido: {l.strip()[:70]}")
            for p, nivel in vaz:
                if p.search(l):
                    R.add("texto", nivel, onde, f"vazamento de processo? ({p.pattern}): {l.strip()[:70]}")
            if cod or l.lstrip().startswith("!["):
                continue
            sem_img = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", l)
            for ref in internas:
                if ref in sem_img:
                    R.add("texto", "ERRO", onde, f"referência a arquivo interno do projeto ({ref}) — o livro deve ser autocontido")
            if re.search(r"\bcap\d\d/", sem_img):
                R.add("texto", "ERRO", onde, "referência a pasta interna capNN/")


# ---------------------------------------------------------------- números e fórmulas
def checa_numeros(arqs, cfg, R):
    dec = cfg["numeros"]["decimal"]
    # números de seção, figura, versão etc. ("seção 3.2", "Figuras 3.4 e 3.5") não são decimais
    ref = re.compile(r"(Figura|Tabela|[Ss]eç(ão|ões)|[Cc]apítulo|Exemplo|Exercício|Passo|Apêndice|item|versão|Python|v)s?"
                     r"\s*([\d.]+\s*(,|e|a)\s*)*$")
    for a in arqs:
        for i, l, cod, form in linhas_texto(a.read_text(encoding="utf-8")):
            if cod or form or l.lstrip().startswith(("#", "![", "|---", "| ---")):
                continue
            onde = f"{rel(a)}:{i}"
            if re.search(r"(?<![\\\w$])(US|R|A|C|NZ)\$\s?\d", l):
                R.add("números", "AVISO", onde, "moeda com cifrão sem escape (use US\\$): o pandoc lê como fórmula")
            for m in re.finditer(r"(?<!\\)\$([^$]+)(?<!\\)\$", re.sub(r"`[^`]*`", "", l)):
                if m.group(1) != m.group(1).strip():
                    R.add("fórmulas", "ERRO", onde, f"espaço junto ao cifrão em ${m.group(1)}$ (o pandoc não reconhece)")
            t = limpa_inline(l)
            if dec == ",":
                for m in re.finditer(r"(?<![\d.,\w])\d+\.\d{1,2}(?![\d\w]|\.\d)", t):
                    if not ref.search(t[: m.start()]):
                        R.add("números", "AVISO", onde, f"'{m.group()}' parece decimal com ponto (no texto use vírgula)")
            if re.search(r"(?<![\w\-–—])-\d", t):
                R.add("números", "AVISO", onde, "hífen como sinal de menos (use −)")
        texto = a.read_text(encoding="utf-8")
        for m in re.finditer(r"_\{([^}]*)\}", texto):
            if re.search(r"[À-ÿ]", m.group(1)) and "\\text" not in m.group(1):
                ln = texto[: m.start()].count("\n") + 1
                R.add("fórmulas", "ERRO", f"{rel(a)}:{ln}", f"acento em subscrito sem \\text{{}}: _{{{m.group(1)}}}")


# ---------------------------------------------------------------- caixas de código e fórmula
def checa_caixas(arqs, cfg, R):
    v = cfg["verificacao"]
    for a in arqs:
        ls = a.read_text(encoding="utf-8").split("\n")
        codigo, lang, inicio = False, "", 0
        for i, l in enumerate(ls):
            s = l.strip()
            if s.startswith("```"):
                if not codigo:
                    codigo, lang, inicio = True, s[3:].strip().strip("{}. "), i + 1
                    if not lang:
                        R.add("código", "AVISO", f"{rel(a)}:{i + 1}", "bloco de código sem linguagem")
                    continue
                codigo = False
                if lang in v["linguagens_sem_caixa"]:
                    continue
                prox = next((x.strip() for x in ls[i + 1:] if x.strip()), "")
                if prox.startswith("```"):
                    continue  # blocos seguidos: a explicação vem depois do último
                if v["caixa_codigo"] not in prox:
                    R.add("código", "ERRO", f"{rel(a)}:{inicio}", f"bloco '{lang or '?'}' sem '> **{v['caixa_codigo']}.**' logo depois")
        # fórmulas destacadas
        texto = "\n".join(ls)
        for m in re.finditer(r"^\$\$.*?\$\$[ \t]*$", texto, re.S | re.M):
            depois = [x for x in texto[m.end():].split("\n") if x.strip()][:3]
            if not any(c in x for x in depois for c in v["caixas_formula"]):
                ln = texto[: m.start()].count("\n") + 1
                R.add("fórmulas", "AVISO", f"{rel(a)}:{ln}", "fórmula destacada sem 'Lendo a fórmula' (ignore se não é nova)")


# ---------------------------------------------------------------- siglas
def siglas_definidas():
    arq = RAIZ / "0s-siglas.md"
    defs = set()
    if arq.exists():
        for l in arq.read_text(encoding="utf-8").split("\n"):
            if l.startswith("|") and not re.match(r"^\|\s*(Sigla|-)", l):
                defs |= {t.strip() for t in re.split(r"[,/]\s*", l.split("|")[1]) if t.strip()}
    return defs


def checa_siglas(arqs, cfg, R):
    v = cfg["verificacao"]
    ign = set(v["siglas_ignoradas"]) | UNIDADES
    defs = siglas_definidas()
    total, onde_1a = collections.Counter(), {}
    caps = {}
    for a in arqs:
        if a.name == "0s-siglas.md":
            continue
        cap = a.parent.name if re.fullmatch(r"cap\d\d", a.parent.name) else a.name
        vistas = caps.setdefault(cap, set())
        paragrafo, ini = [], 1
        for i, l, cod, form in list(linhas_texto(a.read_text(encoding="utf-8"))) + [(10**9, "", False, False)]:
            if cod or form:
                continue
            t = limpa_inline(l)
            achadas = [s for s in SIGLA.findall(t) if s.upper() not in ign and not ROMANO.match(s) and not re.fullmatch(r"[A-Z]\d*", s)]
            for s in achadas:
                total[s] += 1
                onde_1a.setdefault(s, f"{rel(a)}:{i}")
                if s in vistas or l.lstrip()[:1] in ("#", "|"):  # a expansão se cobra no texto corrido
                    continue
                vistas.add(s)
                if not (re.search(rf"\(\s*{s}\b", t) or re.search(rf"\b{s}\s*\(", t)):
                    R.add("siglas", "AVISO", f"{rel(a)}:{i}", f"primeira ocorrência de {s} no capítulo sem expansão")
            if l.strip():
                paragrafo += achadas
                continue
            distintas = set(paragrafo)
            if len(distintas) > v["max_siglas_paragrafo"]:
                R.add("siglas", "AVISO", f"{rel(a)}:{ini}", f"{len(distintas)} siglas no parágrafo ({', '.join(sorted(distintas))}): reescreva por extenso")
            paragrafo, ini = [], i + 1
    for s, n in total.most_common():
        if s not in defs:
            R.add("siglas", "AVISO", onde_1a[s], f"{s} ({n}×) fora de 0s-siglas.md")
        if n < v["min_usos_sigla"]:
            R.add("siglas", "AVISO", onde_1a[s], f"{s} aparece só {n}×: escreva por extenso")


# ---------------------------------------------------------------- tabelas
NUM = re.compile(r"^[−\-+]?\(?[\d.,]+\)?\s*(%|p\.p\.)?$")


def checa_tabelas(arqs, cfg, R):
    maxc = cfg["verificacao"]["max_celula"]
    for a in arqs:
        ls = a.read_text(encoding="utf-8").split("\n")
        i = 0
        codigo = False
        while i < len(ls):
            if ls[i].lstrip().startswith("```"):
                codigo = not codigo
            if codigo or not ls[i].startswith("|") or i + 1 >= len(ls) or not re.match(r"^\|[\s:|-]+\|?\s*$", ls[i + 1]):
                i += 1
                continue
            ini = i
            linhas = []
            while i < len(ls) and ls[i].startswith("|"):
                linhas.append([c.strip() for c in ls[i].strip().strip("|").split("|")])
                i += 1
            onde = f"{rel(a)}:{ini + 1}"
            ant = next((x.strip() for x in reversed(ls[:ini]) if x.strip()), "")
            referencia = any(t in ant for t in cfg["verificacao"]["titulos_tabela_livre"])
            if (ant.startswith("#") or not ant) and not referencia and a.name != "0s-siglas.md":
                R.add("tabelas", "AVISO", onde, "tabela sem texto antes dizendo o que mostra")
            corpo = linhas[2:]
            for r in corpo:
                for c in r:
                    if len(c) > maxc:
                        R.add("tabelas", "AVISO", onde, f"célula com {len(c)} caracteres (parágrafo em tabela?): {c[:50]}…")
            for j in range(1, len(linhas[0])):
                col = [r[j] for r in corpo if j < len(r) and r[j] not in ("", "—", "-", "–", "n/d", "…")]
                nums = [c for c in col if NUM.match(c.replace("**", ""))]
                textos = [c for c in col if not re.search(r"\d", c)]
                if nums and textos:
                    R.add("tabelas", "AVISO", onde, f"coluna '{linhas[0][j][:30]}' mistura números e texto")


# ---------------------------------------------------------------- figuras
LEGENDA = re.compile(r"^!\[Figura ([0-9A-Z]+\.\d+) —")


def checa_figuras(arqs, cfg, R):
    todas = {a: a.read_text(encoding="utf-8") for a in arqs}
    corpo = "\n".join(l for t in todas.values() for l in t.split("\n") if not LEGENDA.match(l))
    n = 0
    for a, t in todas.items():
        for i, l in enumerate(t.split("\n"), 1):
            m = re.match(r"^!\[(.*?)\]\((.*?)\)", l)
            if not m:
                continue
            n += 1
            onde = f"{rel(a)}:{i}"
            if not (RAIZ / m.group(2)).exists():
                R.add("figuras", "ERRO", onde, f"arquivo não existe: {m.group(2)}")
            lm = LEGENDA.match(l)
            if not lm:
                R.add("figuras", "AVISO", onde, "legenda não começa com 'Figura N.M —'")
            elif not re.search(rf"Figuras? (?:[0-9A-Z]+\.\d+ (?:e|a) )?{re.escape(lm.group(1))}(?!\d)", corpo):
                R.add("figuras", "AVISO", onde, f"Figura {lm.group(1)} não é citada no texto (ferramentas/citar_figuras.py)")
    tex = RAIZ / "build" / "livro.tex"
    if tex.exists():
        k = tex.read_text(encoding="utf-8").count("\\includegraphics")
        if k != n:
            R.add("figuras", "ERRO", "build/livro.tex", f"{k} figuras no LaTeX × {n} no Markdown (gere o livro de novo)")
    pdf = RAIZ / "saida" / f"{cfg['saida']}.pdf"
    pdfimages = programa("pdfimages")
    if pdf.exists() and pdfimages:
        r = subprocess.run([pdfimages, "-list", str(pdf)], capture_output=True, text=True)
        k = sum(1 for l in r.stdout.splitlines()[2:] if l.split()[2:3] == ["image"])
        if k < n:
            R.add("figuras", "ERRO", rel(pdf), f"{k} imagens no PDF × {n} figuras no texto: figura perdida?")


# ---------------------------------------------------------------- gabaritos
def checa_gabaritos(cfg, R):
    for cap in cfg["estrutura"]["capitulos"]:
        perg = 0
        for f in capitulo_arquivos(RAIZ, cap):
            for bloco in re.findall(r"^#{2,4}[^\n]*Perguntas de recuperação[^\n]*\n(.*?)(?=^#|\Z)",
                                    f.read_text(encoding="utf-8"), re.S | re.M):
                perg += len(re.findall(r"^\d+\. ", bloco, re.M))
        g = RAIZ / "apendices" / f"G-recuperacao-{cap}.md"
        resp = len(re.findall(r"^\*\*\d+\. ", g.read_text(encoding="utf-8"), re.M)) if g.exists() else 0
        if perg != resp:
            R.add("gabaritos", "ERRO", cap, f"{perg} perguntas de recuperação × {resp} respostas no Apêndice G")
        if not (RAIZ / "apendices" / f"G-solucoes-{cap}.md").exists():
            R.add("gabaritos", "ERRO", cap, "sem soluções dos exercícios (apendices/G-solucoes-capNN.md)")
        texto = "\n".join(f.read_text(encoding="utf-8") for f in capitulo_arquivos(RAIZ, cap))
        if not re.search(r"^#{2,4} .*(Fontes|Referências)", texto, re.M):
            R.add("gabaritos", "AVISO", cap, "capítulo sem seção de fontes e referências")


# ---------------------------------------------------------------- log do LaTeX
def checa_log(cfg, R):
    log = RAIZ / "build" / "livro.log"
    if not log.exists():
        R.add("latex", "AVISO", "build/livro.log", "log não encontrado: gere o livro antes")
        return
    s = log.read_text(encoding="utf-8", errors="replace")
    for m in re.findall(r"Missing character: There is no (.) .*", s)[:50]:
        R.add("latex", "ERRO", "build/livro.log", f"glifo ausente: {m!r} (acento em subscrito? símbolo sem fonte?)")
    k = s.count("Overfull \\vbox")
    if k:
        R.add("latex", "ERRO", "build/livro.log", f"{k} Overfull \\vbox (página ou figura estourada)")
    tol = cfg["verificacao"]["hbox_tolerancia_pt"]
    for pt, linhas in re.findall(r"Overfull \\hbox \(([\d.]+)pt too wide\) [^\n]*?lines? ([\d-]+)", s):
        if float(pt) > tol:
            R.add("latex", "AVISO", "build/livro.tex", f"linha {linhas}: {pt} pt além da margem")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grupo", nargs="*", help="texto números fórmulas código siglas tabelas figuras gabaritos latex")
    ap.add_argument("--max", type=int, default=40)
    a = ap.parse_args()
    cfg = carregar_config()
    arqs = arquivos_livro(cfg)
    R = Relatorio(a.max)
    checa_texto(arqs, cfg, R)
    checa_numeros(arqs, cfg, R)
    checa_caixas(arqs, cfg, R)
    checa_siglas(arqs, cfg, R)
    checa_tabelas(arqs, cfg, R)
    checa_figuras(arqs, cfg, R)
    checa_gabaritos(cfg, R)
    checa_log(cfg, R)
    erros = R.imprime(set(a.grupo) if a.grupo else None)
    print("Itens que só a leitura encontra (origem de cada número, conversões, bases misturadas): agente revisor-leitor.")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
