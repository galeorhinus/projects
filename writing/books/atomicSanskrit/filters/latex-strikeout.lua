-- Use ulem for PDF strikeout so the build does not depend on soul.sty.
function Strikeout(element)
  if not FORMAT:match("latex") then
    return nil
  end

  local result = { pandoc.RawInline("latex", "\\sout{") }
  for _, inline in ipairs(element.content) do
    result[#result + 1] = inline
  end
  result[#result + 1] = pandoc.RawInline("latex", "}")
  return result
end
