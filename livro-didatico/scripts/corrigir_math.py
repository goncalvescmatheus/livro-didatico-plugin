"""Remove espaços logo após o $ de abertura e logo antes do $ de fechamento da matemática inline
(o pandoc não reconhece "$ x$" nem "$x $" como fórmula). Ignora blocos de código, código inline e $$.

Não mexe em moedas: escapar "US$" automaticamente já corrompeu fórmulas. Moedas sem escape são
apontadas por verificar_livro.py e corrigidas à mão. Revise o diff depois de rodar.

Uso: python3 ferramentas/corrigir_math.py capNN/*.md ...   (imprime quantas correções fez por arquivo)
"""
import sys


def corrigir_linha(l):
    if "$$" in l:
        return l, 0
    pos, cod, i = [], False, 0
    while i < len(l):
        ch = l[i]
        if ch == "`":
            cod = not cod
        elif ch == "\\":
            i += 2
            continue
        elif ch == "$" and not cod:
            pos.append(i)
        i += 1
    if len(pos) < 2 or len(pos) % 2:  # número ímpar de cifrões: ambíguo, não mexe
        return l, 0
    out, ultimo, n = [], 0, 0
    for a, b in zip(pos[0::2], pos[1::2]):
        dentro = l[a + 1:b]
        novo = dentro.strip()
        n += novo != dentro
        out += [l[ultimo:a + 1], novo]
        ultimo = b
    out.append(l[ultimo:])
    return "".join(out), n


def main():
    for f in sys.argv[1:]:
        linhas, bloco, tot = open(f, encoding="utf-8").read().split("\n"), False, 0
        for k, l in enumerate(linhas):
            if l.lstrip().startswith("```"):
                bloco = not bloco
                continue
            if not bloco:
                novo, n = corrigir_linha(l)
                if n:
                    linhas[k], tot = novo, tot + n
        if tot:
            open(f, "w", encoding="utf-8").write("\n".join(linhas))
            print(f, tot)


if __name__ == "__main__":
    assert corrigir_linha("custo $ c_t$ e $x $ fim")[0] == "custo $c_t$ e $x$ fim"
    assert corrigir_linha("preço US\\$ 5 e $p$")[1] == 0
    main()
