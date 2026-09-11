local map = vim.keymap.set

map("i", "jk", "<Esc>", { noremap = true, desc = "exit insert mode" })

map("n", "<Esc>", "<cmd>noh<CR>", { silent = true, desc = "clear search highlight" })

map("n", "<leader>q", "<cmd>q<CR>", { desc = "quit buffer" })
map("n", "<leader>w", "<cmd>w<CR>", { desc = "save buffer" })

map("n", "q", "<Nop>", { desc = "disable single q" })

map({ "n", "v" }, "<leader>y", '"+y', { desc = "copy to system clipboard" })
