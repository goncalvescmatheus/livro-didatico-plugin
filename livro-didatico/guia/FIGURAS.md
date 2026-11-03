# Guia de figuras

As figuras ensinam; não decoram. O estilo comum está em `codigo/figuras/estilo.py`.

## 1. Regras obrigatórias

1. **Toda curva, função ou relação mencionada no texto tem gráfico ou diagrama.**
2. **Sem linhas de grade.**
3. **Nenhum texto ou legenda sobre as curvas:** a legenda fica abaixo da área do gráfico (`legenda_abaixo`).
4. **Linhas de chamada** tracejadas até os eixos, com o **valor exato** nos pontos que o texto cita (`chamada`).
5. **Números no padrão do idioma** também nos eixos (vírgula decimal, ponto de milhar, sinal de menos "−"): `fmt()` e a formatação automática de `salvar()`.
6. **Cores semânticas fixas:** o mesmo conceito tem a mesma cor em todo o livro (dicionário `COR`, preenchido no início do projeto).
7. **Tamanho compatível com a página:** largura máxima de 8,5 polegadas, para que o texto impresso não fique abaixo de cerca de 7 pt. O estilo limita isso sozinho.
8. **Didática acima da estética.** Se a biblioteca padrão não der conta, use outra (aberta).
9. **Abra e inspecione cada imagem** depois de gerar: sobreposição, texto cortado, legenda sobre curva, símbolo cru (`_`, `^` fora de `$...$`), unidade faltando. `salvar()` emite avisos para parte desses casos.
10. **Sem título dentro da figura** que repita a legenda; título de painel só quando há vários painéis.
11. **Unidade em todo eixo**; rótulos por extenso, sem siglas criadas pelo livro.
12. **Os números da figura são os do texto**, produzidos pelo mesmo código.

## 2. Legenda e citação

- Sintaxe: `![Figura N.M — {{frase completa: o que a figura mostra e a conclusão}}.](figuras/capNN/fN_MM_nome.png){width=95%}`
- A numeração é manual, no texto da legenda; a numeração automática do LaTeX fica desligada.
- **Toda figura é citada no texto** ("(Figura N.M)"). `ferramentas/citar_figuras.py` acrescenta a citação que falta ao parágrafo anterior; revise o resultado.
- Arquivos em `figuras/capNN/`, gerados por `codigo/figuras/fig_capNN.py`, uma função por figura.

## 3. Tipos que funcionam bem

| Tipo | Para quê |
| --- | --- |
| Esquema de fluxo ou de sequência | Processos, mercados, estruturas de contrato, árvores de decisão |
| Gráfico com chamadas | Curvas com pontos citados no texto |
| Cascata (*waterfall*) | Decompor um valor em parcelas |
| Fronteira e sensibilidade (tornado, barras por cenário) | Trocas entre média e risco; o que mais move o resultado |
| Mapa de calor | Padrões por duas dimensões (mês × hora) |
| Real × modelo | Calibração e validação |
| Pequenos múltiplos | Comparar cenários lado a lado com eixos iguais |

## 4. Esqueleto de uma figura

```python
from estilo import plt, COR, chamada, legenda_abaixo, salvar, fmt

def fig_3_2_curva(dados):
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(dados.x, dados.y, color=COR["conceito_a"], label="Conceito A")
    ax.set_xlabel("Grandeza (unidade)")
    ax.set_ylabel("Grandeza (unidade)")
    chamada(ax, x=6.09, y=3000, texto=f"{fmt(6.09, 2)} h; {fmt(3000)} €")
    legenda_abaixo(ax, ncol=2)
    salvar(fig, "figuras/cap03/f3_02_curva.png")
```
