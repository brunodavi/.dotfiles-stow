return {
  "neovim/nvim-lspconfig",
  ft = {
    "javascript",
    "typescript",
    "typescriptreact",
    "javascriptreact",
    "python",
    "c",
    "cpp",
    "cs",
    "go",
    "dart",
    "nim",
  },
  dependencies = {
    "hrsh7th/cmp-nvim-lsp",
  },
  config = function()
    -- Certifique-se de que o seu utils.lua está em lua/plugins/lsp/utils.lua
    -- ou ajuste o require abaixo caso tenha movido para lua/lsp/utils.lua
    local utils = require("plugins.lsp.utils")

    -- 1. Configurações globais que valem para TODOS os servidores
    vim.lsp.config("*", {
      capabilities = utils.capabilities,
      on_attach = utils.on_attach,
    })

    -- 2. Caminho absoluto até a pasta dos servidores
    local servers_dir = vim.fn.stdpath("config") .. "/lua/plugins/lsp/servers"

    if vim.fn.isdirectory(servers_dir) == 1 then
      local files = vim.fn.readdir(servers_dir, function(name)
        return vim.endswith(name, ".lua")
      end)

      for _, file in ipairs(files) do
        local server_name = file:sub(1, -5)

        -- Carrega o arquivo dentro de lua/plugins/lsp/servers/
        local custom_config = require("plugins.lsp.servers." .. server_name)

        -- Se houver tabela de configuração customizada no arquivo
        if type(custom_config) == "table" and next(custom_config) ~= nil then
          vim.lsp.config(server_name, custom_config)
        end

        -- Habilita o servidor
        vim.lsp.enable(server_name)
      end
    end
  end,
}
