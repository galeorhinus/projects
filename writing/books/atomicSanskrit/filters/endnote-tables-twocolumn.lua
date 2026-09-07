--[[
Make the companion's endnote tables survive a two-column endnotes section.

Pandoc writes every pipe table as a `longtable`, and longtable fails outright
in two-column mode -- "longtable not in 1-column mode", an error, not a
cosmetic problem. A table inside the two-column endnotes therefore has to
become a `table*` float (which spans both columns) wrapping a plain `tabular`.

Scope matters more than the conversion. The reference appendices ahead of the
endnotes hold 27 tables and 241 rows, and they stay single-column precisely
because they need longtable to break across pages; rewriting those to tabular
would push long tables off the bottom of a page with no way to continue. So
the rewrite starts only once the Endnotes header has gone by, which in the
companion is also exactly where \twocolumn takes effect.
--]]

local in_endnotes = false

-- Turn one rendered longtable into a full-width float. The header/footer
-- markers are longtable's own pagination machinery and have no meaning in a
-- tabular; \bottomrule is re-added at the end because pandoc emits it up front
-- as part of \endlastfoot.
local function longtable_to_table_star(latex)
  local body = latex:gsub("\\begin{longtable}%[%]", "\\begin{tabular}")
                    :gsub("\\begin{longtable}", "\\begin{tabular}")
                    :gsub("\\end{longtable}", "\\end{tabular}")
                    :gsub("\\endfirsthead", "")
                    :gsub("\\endhead", "")
                    :gsub("\\endfoot", "")
                    :gsub("\\bottomrule\\noalign{}\n\\endlastfoot", "")
                    :gsub("\\endlastfoot", "")
  body = body:gsub("\\end{tabular}", "\\bottomrule\\noalign{}\n\\end{tabular}")
  return table.concat({
    "\\begin{table*}[t]", "\\centering", "\\small",
    body,
    "\\end{table*}",
  }, "\n")
end

-- A float can only be placed at the top of a page, so one taller than that
-- space is deferred, and a table taller than a whole page can never be placed
-- at all: the 46-row Schleicher fable comparison drifted 38 pages past its own
-- note, to the end of the volume. A tall table has to keep its longtable and
-- therefore has to leave two-column mode, which costs a page break either side
-- but keeps the table with the note that discusses it.
local function longtable_single_column(latex)
  return table.concat({ "\\onecolumn", latex, "\\twocolumn" }, "\n")
end

-- Rows past which a table cannot be trusted to place as a float. Six of the
-- seven endnote tables sit at or under seven rows; only the fable comparison
-- is anywhere near this.
local TALL_TABLE_ROWS = 15

local function row_count(tbl)
  local n = 0
  for _, body in ipairs(tbl.bodies or {}) do
    n = n + #(body.body or {})
  end
  return n
end

function Pandoc(doc)
  local out = {}
  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 1
       and pandoc.utils.stringify(block):match("^Endnotes") then
      in_endnotes = true
    end
    if in_endnotes and block.t == "Table" then
      local rendered = pandoc.write(pandoc.Pandoc({ block }), "latex")
      local latex = row_count(block) > TALL_TABLE_ROWS
        and longtable_single_column(rendered)
        or longtable_to_table_star(rendered)
      out[#out + 1] = pandoc.RawBlock("latex", latex)
    else
      out[#out + 1] = block
    end
  end
  return pandoc.Pandoc(out, doc.meta)
end
