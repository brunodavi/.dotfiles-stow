local M = {}

local ok, cmp_nvim_lsp = pcall(require, "cmp_nvim_lsp")

if ok then
  M.capabilities = cmp_nvim_lsp.default_capabilities()
else
  M.capabilities = vim.lsp.protocol.make_client_capabilities()
end

M.on_attach = function(_, bufnr)
  local opts = { buffer = bufnr, silent = true }
  local keymap = vim.keymap.set

  opts.desc = "go to definitions"
  keymap("n", "gd", vim.lsp.buf.definition, opts)

  opts.desc = "see docs"
  keymap("n", "K", vim.lsp.buf.hover, opts)

  opts.desc = "rename symbol"
  keymap("n", "<leader>rn", vim.lsp.buf.rename, opts)

  opts.desc = "code actions"
  keymap("n", "<leader>ca", vim.lsp.buf.code_action, opts)
end

return M
