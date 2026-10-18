return {
    {
        "folke/flash.nvim",
        event = "VeryLazy",
        opts = {
            search = {
                mode = "exact",
                max_length = 2,
            },
            jump = {
                autojump = true,
            },
            label = {
                after = true,
                before = false,
                uppercase = false,
                distance = true,
            },
        },
        keys = {
            {
                "s",
                mode = { "n", "x", "o" },
                function()
                    require("flash").jump({
                        search = {
                            mode = "exact",
                            max_length = 2,
                        },
                        jump = {
                            autojump = true,
                        },
                    })
                end,
                desc = "Flash: jump",
            },
            {
                "S",
                mode = { "n", "x", "o" },
                function()
                    require("flash").treesitter()
                end,
                desc = "Flash: Treesitter",
            },
        },
    },
}
