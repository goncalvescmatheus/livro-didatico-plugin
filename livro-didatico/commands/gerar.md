---
description: Gera o livro (PDF via LaTeX e Word) e roda as verificações automáticas e visuais
---

1. Se `python3 ferramentas/verificar_ambiente.py` apontar falta de pandoc ou Tectonic, mostre o que falta e **peça permissão** antes de instalar.
2. `python3 ferramentas/gerar_livro.py`
3. `python3 ferramentas/verificar_livro.py`: corrija todos os ERROS; revise cada AVISO e diga ao usuário quais são legítimos.
4. `python3 ferramentas/amostrar_paginas.py` e abra as imagens de `build/paginas/`: capa, sumário, aberturas de capítulo e páginas sorteadas. Procure figura cortada ou ausente, tabela estourando a margem, fórmula quebrada, código ilegível.
5. Informe: número de páginas, de figuras, erros corrigidos, avisos mantidos e por quê.
