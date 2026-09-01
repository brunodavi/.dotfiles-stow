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
vim.g.netrw_winsize = 25
vim.g.netrw_browse_split = 4


-- FUNÇÕES LUA

local function toggle_explorer()
  local netrw_win = nil

  for _, win in ipairs(vim.api.nvim_list_wins()) do
    local buf = vim.api.nvim_win_get_buf(win)
    if vim.bo[buf].filetype == "netrw" then
      netrw_win = win
      break
    end
  end

  if netrw_win then
    vim.api.nvim_win_close(netrw_win, true)
  else
    vim.cmd("Lexplore")
  end
end


-- MAPEAMENTO DE TECLAS

local map = vim.keymap.set

map("n", "<Esc>", "<cmd>noh<CR>", { silent = true })

map("n", "<leader>w", "<cmd>w<CR>")
map("n", "<leader>q", "<cmd>q<CR>")

map("i", "jk", "<Esc>", { noremap = true })

map("n", "<leader>bn", "<cmd>bnext<CR>")
map("n", "<leader>bp", "<cmd>bprevious<CR>")

map("n", "<leader>e", toggle_explorer)

-- Proteção do Clipboard
map({ "n", "v" }, "c", '"_c')
map({ "n", "v" }, "C", '"_C')
map({ "n", "v" }, "x", '"_x')
