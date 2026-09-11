local map = vim.keymap.set

map("i", "jk", "<Esc>", { noremap = true })

map("n", "<Esc>", "<cmd>noh<CR>", { silent = true })

map("n", "<leader>q", "<cmd>q<CR>")
map("n", "<leader>w", "<cmd>w<CR>")

map("n", "q", "<Nop>")

map({ "n", "v" }, "<leader>y", '"+y')
