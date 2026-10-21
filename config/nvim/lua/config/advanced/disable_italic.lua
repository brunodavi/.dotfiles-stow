-- Remove o itálico de TODOS os highlights.
--
-- Motivo: no Termux o terminal não renderiza itálico direito
-- (o texto fica cortado).
--
-- Como funciona:
--   • autocmd `ColorScheme`: roda depois de qualquer tema (tokyonight,
--     one dark, ...)
--   • `defer_fn`: o treesitter recria os grupos `@markup.*` depois do
--     colorscheme, então passamos de novo um pouco mais tarde

local function disable_italics()
  for name, hl in pairs(vim.api.nvim_get_hl(0, {})) do
    if hl.italic ~= nil then
      if hl.link then
        vim.api.nvim_set_hl(0, name, { link = hl.link })
      else
        hl.italic = nil
        vim.api.nvim_set_hl(0, name, hl)
      end
    end
  end
end

vim.api.nvim_create_autocmd("ColorScheme", {
  pattern = "*",
  callback = disable_italics,
})

vim.defer_fn(disable_italics, 150)
