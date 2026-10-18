return {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    opts = {
        on_attach = function(bufnr)
            local gs = require("gitsigns")

            vim.keymap.set("n", "<leader>hp", gs.preview_hunk, {
                buffer = bufnr,
                desc = "Preview Git hunk",
            })

            vim.keymap.set("n", "<leader>hr", gs.reset_hunk, {
                buffer = bufnr,
                desc = "Reverter alterações do bloco",
            })
        end,

    },
}
