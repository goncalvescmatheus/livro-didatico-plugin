"""Gera o glossário consolidado (Apêndice F) juntando as tabelas de glossário dos capítulos.
A tabela é escrita só entre os marcadores do arquivo do apêndice; o texto escrito à mão fora deles é preservado.
Nada no texto gerado menciona arquivos ou ferramentas do projeto (o livro é autocontido).

Formato esperado em cada capítulo: um título contendo "Glossário" seguido de uma tabela cuja primeira coluna é o termo.
Uso: python3 ferramentas/gerar_glossario.py
"""
import re
import sys
import unicodedata

from _comum import RAIZ, capitulo_arquivos, carregar_config

INI, FIM = "<!-- início da tabela gerada -->", "<!-- fim da tabela gerada -->"


def chave(t):
    return unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()


def main():
    cfg = carregar_config()
    termos, cabecalho = {}, None
    for cap in cfg["estrutura"]["capitulos"]:
        for f in capitulo_arquivos(RAIZ, cap):
            s = f.read_text(encoding="utf-8")
            m = re.search(r"^#{2,4} [^\n]*Glossário[^\n]*\n", s, re.M)
            if not m:
                continue
            tabela = []
            for l in s[m.end():].split("\n"):
                if l.startswith("|"):
                    tabela.append([c.strip() for c in l.strip().strip("|").split("|")])
                elif tabela:
                    break
            if len(tabela) < 3:
                continue
            cabecalho = cabecalho or tabela[0]
            for linha in tabela[2:]:
                termos.setdefault(chave(linha[0]), [linha, set()])[1].add(str(int(cap[3:])))
    if not termos:
        sys.exit("nenhuma tabela de glossário encontrada nos capítulos")

    linhas = ["| " + " | ".join(cabecalho + ["Capítulos"]) + " |", "|" + " --- |" * (len(cabecalho) + 1)]
    for k in sorted(termos):
        linha, caps = termos[k]
        linha = (linha + [""] * len(cabecalho))[: len(cabecalho)]
        linhas.append("| " + " | ".join(linha + [", ".join(sorted(caps, key=int))]) + " |")
    tabela = "\n".join(linhas)

    arq = next(iter(sorted((RAIZ / "apendices").glob("F-*.md"))), RAIZ / "apendices" / "F-glossario.md")
    s = arq.read_text(encoding="utf-8") if arq.exists() else f"# Apêndice F — Glossário\n\n{INI}\n{FIM}\n"
    if INI not in s or FIM not in s:
        s = s.rstrip("\n") + f"\n\n{INI}\n{FIM}\n"
    antes, resto = s.split(INI, 1)
    depois = resto.split(FIM, 1)[1]
    arq.write_text(f"{antes}{INI}\n{tabela}\n{FIM}{depois}", encoding="utf-8")
    print(f"{len(termos)} termos em {arq.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
