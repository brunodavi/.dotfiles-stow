return {
  {
    "echasnovski/mini.nvim",
    -- carrega só o módulo mini.pick (buscador de arquivos/texto)
    version = false,
    keys = {
      { "<leader>f", function() require("mini.pick").builtin.files() end, desc = "mini.pick: arquivos" },
      { "<leader>/", function() require("mini.pick").builtin.grep_live() end, desc = "mini.pick: texto nos arquivos" },
      { "<leader>b", function() require("mini.pick").builtin.buffers() end, desc = "mini.pick: buffers" },
      { "<leader>h", function() require("mini.pick").builtin.help() end, desc = "mini.pick: help tags" },
    },
    config = function()
      require("mini.pick").setup()
    end,
  },
}
