-- Let long inline identifiers and file paths wrap in PDF output.
-- Pandoc's default \texttt{...} is an unbreakable box; \path from url.sty
-- preserves the monospaced appearance while allowing breaks at separators.
local function breakable_code(element)
  if not FORMAT:match("latex") then
    return nil
  end

  local value = element.text
  if #value < 24 or not value:find("[-_/.]") then
    return nil
  end

  for _, delimiter in ipairs({ "|", "!", "+", "=", ";", ":" }) do
    if not value:find(delimiter, 1, true) then
      return pandoc.RawInline("latex", "\\path" .. delimiter .. value .. delimiter)
    end
  end

  -- Extremely unusual code spans containing every delimiter retain Pandoc's
  -- default rendering instead of risking malformed LaTeX.
  return nil
end

function Pandoc(document)
  if not FORMAT:match("latex") then
    return nil
  end

  local blocks = {}
  for _, block in ipairs(document.blocks) do
    -- Section headings become PDF bookmarks and other moving arguments;
    -- url.sty's \path command is intentionally unavailable there.
    if block.t == "Header" then
      blocks[#blocks + 1] = block
    else
      blocks[#blocks + 1] = block:walk({ Code = breakable_code })
    end
  end
  document.blocks = blocks
  return document
end
