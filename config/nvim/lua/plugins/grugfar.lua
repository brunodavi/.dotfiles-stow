return {
  {
    "MagicDuck/grug-far.nvim",
    -- regex, busca e replace em todo o projeto com preview de diff
    keys = {
      { "<leader>r", function() require("grug-far").open() end, desc = "grug-far: search/replace" },
    },
    config = function()
      require("grug-far").setup({
        -- split horizontal cabe melhor na tela do celular que o tabnew padrão
        windowCreationCommand = "botright 60new",
      })
    end,
  },
}
