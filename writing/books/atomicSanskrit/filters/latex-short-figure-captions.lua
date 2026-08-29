-- Keep the complete caption beneath each figure while using only its first
-- sentence in LaTeX's List of Figures. The manuscript caption remains the
-- single source of truth; this filter derives the short form at build time.

local function ends_sentence(inline)
  local text = pandoc.utils.stringify(inline)
  return text:match("[%.%!%?][\"')%]]*$") ~= nil
end

local function first_sentence(blocks)
  if #blocks == 0 then
    return nil
  end

  local source = blocks[1].content
  if source == nil then
    return nil
  end

  local short = pandoc.Inlines({})
  local found_end = false

  for _, inline in ipairs(source) do
    short:insert(inline)
    if ends_sentence(inline) then
      found_end = true
      break
    end
  end

  -- A fragmentary caption has no shorter form worth manufacturing.
  if not found_end or #short == #source then
    return nil
  end

  return short
end

function Figure(figure)
  if not FORMAT:match("latex") then
    return nil
  end

  local short = first_sentence(figure.caption.long)
  if short ~= nil then
    figure.caption.short = short
    return figure
  end

  return nil
end
