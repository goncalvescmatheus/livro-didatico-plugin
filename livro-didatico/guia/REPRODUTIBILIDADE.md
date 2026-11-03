# Guia de reprodutibilidade e ferramentas abertas

O leitor deve conseguir refazer cada número do livro com o código do livro, dados públicos e ferramentas gratuitas. Isso também protege o autor: quando uma premissa muda, a cadeia inteira é refeita sem caça manual a números.

---

## 1. A regra de ouro dos números

**Todo número do livro sai de código executado antes de entrar no texto.**

- Os scripts ficam em `codigo/capNN/`, um por exemplo ou por tabela, com nome que diz o que produzem (`exemplo_3_2_collar.py`).
- Cada script imprime os números que o texto usa, já arredondados como no texto, para a comparação ser direta.
- **Sementes fixas** em toda simulação (`rng = np.random.default_rng(20261012)`), registradas na memória do projeto.
- Texto, tabelas, figuras e gabaritos usam o mesmo número. Os números-chave ficam numa tabela da memória do projeto.
- **Quando uma premissa muda:** rode de novo a cadeia (dados → cálculo → figuras → tabelas), atualize todas as ocorrências e faça uma busca pelo número antigo em todos os arquivos (`grep -rn "12,5" cap*/ apendices/`).
- Contas que o texto faz "à mão" também são conferidas em código.

## 2. Dados

- **Abertos e públicos** sempre que existirem. Prefira a fonte oficial ao agregador; se usar um agregador, valide contra a oficial numa amostra e registre o resultado.
- Todo download é feito por **script versionado**, nunca à mão. O livro mostra o código de acesso ao leitor.
- Guarde os dados brutos (`dados/brutos/`) separados dos processados (`dados/processados/`), em formatos abertos (CSV, Parquet).
- Registre cada fonte em `dados/FONTES.md`: URL, data de acesso, licença, período, unidade, fuso, revisões conhecidas.
- Erros clássicos a tratar e explicar ao leitor: fuso horário e horário de verão, mudança de granularidade, revisões de séries, unidades, valores ausentes.
- Dados com licença restritiva: só para uso privado, com nota de licença no livro e instrução de como o leitor obtém da fonte oficial.

## 3. Ferramentas: preferência por abertas

Em ordem de preferência, para pacotes, modelos, solvers, bases de dados e APIs:

1. **Código aberto e gratuito**, mantido por comunidade ativa (ex.: Python, NumPy, pandas, SciPy, statsmodels, scikit-learn, matplotlib, HiGHS, pandoc, Tectonic).
2. **Modelos abertos** da área (modelos de sistema, de clima, de mercado, de linguagem com pesos abertos), com versão e configuração registradas.
3. **APIs públicas** com documentação aberta, chamadas por código mostrado no livro; tokens em variáveis de ambiente.
4. **Proprietário** só quando não houver alternativa aberta razoável. Nesse caso, uma **Nota honesta** diz o que o leitor precisa para reproduzir e oferece um caminho aberto aproximado.

Ao escolher uma ferramenta, registre na memória: nome, versão, licença e por que foi escolhida.

## 4. Ambiente

- Python em ambiente virtual do projeto (`.venv`), com as dependências em `requirements.txt` e versões mínimas fixadas. Ao terminar o livro, congele as versões usadas (`pip freeze > requirements-lock.txt`).
- `ferramentas/verificar_ambiente.py` lista o que falta. **Nada é instalado sem permissão do usuário** (ver `REQUISITOS.md`).
- Se vários processos de álgebra linear rodarem em paralelo, use `OMP_NUM_THREADS=1`.
- O laboratório do livro ensina o leitor a montar o mesmo ambiente (Apêndice B).

## 5. Verificação cruzada

Sempre que possível, confira um resultado por um caminho independente:

| Resultado | Conferência |
| --- | --- |
| Solução de otimização | Dualidade forte; conta à mão num caso pequeno |
| Preço por fórmula fechada | Simulação de Monte Carlo com intervalo de confiança |
| Simulação | Caso limite com resposta conhecida |
| Estimativa estatística | Outra especificação; fora da amostra |
| Série baixada | Amostra conferida contra a fonte oficial |

Testes de propriedade (uma desigualdade teórica, uma soma que fecha) valem mais que testes de número exato. Eles entram no laboratório do leitor.

## 6. O que fica registrado

| Onde | O quê |
| --- | --- |
| `codigo/capNN/` | Scripts que produzem cada número, tabela e figura |
| `dados/FONTES.md` | Origem, licença e tratamento de cada dado |
| `MEMORIA_DO_PROJETO.md` | Números-chave, sementes, versões de ferramentas, decisões |
| `requirements.txt` / `requirements-lock.txt` | Ambiente |
| Livro (fim de cada capítulo) | Fontes e datas, para o leitor |
