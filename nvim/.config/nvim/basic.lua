-- CONFIGURAÇÕES GERAIS

vim.g.mapleader = " "

vim.opt.wrap = false
vim.opt.number = true
vim.opt.relativenumber = true

vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.expandtab = true

vim.opt.scrolloff = 8
vim.opt.incsearch = true
vim.opt.ignorecase = true
vim.opt.smartcase = true

vim.g.netrw_banner = 0
vim.g.netrw_sort_by = 'exten'

-- FUNÇÕES LUA

local function find_netrw_win()
  for _, win in ipairs(vim.api.nvim_list_wins()) do
    local buf = vim.api.nvim_win_get_buf(win)
    if vim.bo[buf].filetype == "netrw" then
      return win
    end
  end
  return nil
end

local function close_or_return(win)
  if vim.api.nvim_get_current_win() == win then
    -- volta para o buffer anterior em vez de fechar a última janela
    vim.cmd("b#")
  else
    vim.api.nvim_win_close(win, true)
  end
end

local function toggle_explorer(style)
  local win = find_netrw_win()
  if win then
    close_or_return(win)
    return
  end
  vim.g.netrw_liststyle = style
  vim.w.netrw_liststyle = nil
  vim.cmd("Explore")
  vim.g.netrw_liststyle = 1
end


-- MAPEAMENTO DE TECLAS

local map = vim.keymap.set

map("n", "<Esc>", "<cmd>noh<CR>", { silent = true })

map("n", "<leader>w", "<cmd>w<CR>")
map("n", "<leader>q", "<cmd>q<CR>")

map("i", "jk", "<Esc>", { noremap = true })

map("n", "<leader>bn", "<cmd>bnext<CR>")
map("n", "<leader>bp", "<cmd>bprevious<CR>")

map("n", "<leader>e", function()
  toggle_explorer(1)
end)
map("n", "<leader>E", function()
  toggle_explorer(3)
end)

-- Proteção do Clipboard
map({ "n", "v" }, "c", '"_c')
map({ "n", "v" }, "C", '"_C')
map({ "n", "v" }, "x", '"_x')
