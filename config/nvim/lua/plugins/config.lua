return {
  {
    dir = vim.fn.stdpath("config"),
    lazy = false,
    priority = 1000,
    config = function()
      require("config.options")
      require("config.keymaps")
    end,
  },
}
