return {
  "nvim-treesitter/nvim-treesitter",
  lazy = false,
  build = ":TSUpdate",
  config = function()
    local ts = require("nvim-treesitter")

    ts.setup({
      install_dir = vim.fn.stdpath("data") .. "/site",
    })

    ts.install({
      "nim",
      "c",
      "cpp",
      "c_sharp",
      "dart",
      "go",
      "python",
      "javascript",
      "typescript",
      "tsx",
      "lua",
      "vim",
      "vimdoc",
      "query",
      "json",
      "yaml",
      "toml",
      "bash",
    })

    vim.api.nvim_create_autocmd("FileType", {
      callback = function()
        pcall(vim.treesitter.start)
      end,
    })
  end,
}
