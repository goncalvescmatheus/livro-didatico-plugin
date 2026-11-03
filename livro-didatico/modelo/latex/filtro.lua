-- Filtro pandoc para o livro em LaTeX:
-- 1) blocos de código sem linguagem viram Verbatim (fvextra) com quebra de linha automática;
-- 2) blocos com linguagem mantêm o realce, e o ambiente Highlighting também quebra linhas (ver cabecalho.tex).
function CodeBlock(el)
  if FORMAT:match("latex") and (#el.classes == 0 or el.classes[1] == "text") then
    return pandoc.RawBlock("latex", "\\begin{Verbatim}[breaklines,breakanywhere,fontsize=\\small]\n" .. el.text .. "\n\\end{Verbatim}")
  end
end
