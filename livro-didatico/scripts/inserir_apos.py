"""Insere um texto (por exemplo, uma caixa "Lendo o código") logo depois do bloco de código cuja última linha
é `ancora`. Falha se a âncora não for única, para não editar o lugar errado.

Uso como módulo:  from inserir_apos import inserir; inserir("cap03/04_lab.md", "print(resultado)", texto)
"""


def inserir(arquivo, ancora, texto):
    s = open(arquivo, encoding="utf-8").read()
    alvo = ancora.rstrip("\n") + "\n```\n"
    assert s.count(alvo) == 1, (arquivo, ancora, s.count(alvo))
    s = s.replace(alvo, alvo + "\n" + texto.strip("\n") + "\n", 1)
    open(arquivo, "w", encoding="utf-8").write(s)
