return {
  "akinsho/bufferline.nvim",
  event = "VeryLazy",
  keys = {
    { "<tab>", "<cmd>BufferLineCycleNext<CR>", desc = "buffer goto next" },
    { "<S-tab>", "<cmd>BufferLineCyclePrev<CR>", desc = "buffer goto prev" },
    { "<leader>x", "<cmd>BufferLineCloseOthers<CR>", desc = "buffer close others" },
    { "<leader>c", "<cmd>bd<CR>", desc = "buffer close current" },
  },
  config = function()
    local bufferline = require "bufferline"
    bufferline.setup({
      options = {
        mode = "buffers",
        diagnostics = "nvim_lsp",
        always_show_bufferline = true,
        show_buffer_close_icons = true,
        show_close_icon = false,
        offsets = {
          {
            filetype = "NvimTree",
            text = "File Explorer",
            highlight = "Directory",
            padding = 1,
          },
        },
      },
    })
  end,
}