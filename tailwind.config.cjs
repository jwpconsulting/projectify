module.exports = {
    mode: "jit",
    purge: ["./src/**/*.svelte"],
    content: ["./src/**/*.{html,js,svelte,ts}"],

    theme: {
        colors: {},
        extend: {
            fontFamily: {
                Rampart: ["Roboto", "sans-serif"],
            },
            boxShadow: {
                card: "0px 0px 4px 0px #1E202940",
            },
        },
    },

    variants: {
        display: [
            "children",
            "default",
            "children-first",
            "children-last",
            "children-odd",
            "children-even",
            "children-not-first",
            "children-not-last",
            "children-hover",
            "hover",
            "children-focus",
            "focus",
            "children-focus-within",
            "focus-within",
            "children-active",
            "active",
            "children-visited",
            "visited",
            "children-disabled",
            "disabled",
            "responsive",
        ],
    },

    plugins: [
        require("@tailwindcss/typography"),
        require("tailwindcss-children"),
        require("daisyui"),
    ],

    daisyui: {
        styled: true,
        themes: [
            {
                "app-light": {
                    "fontFamily": "Roboto, sans-serif",
                    "primary": "#76B4F9" /* Primary color */,
                    "primary-focus": "#B5D7FF" /* Primary color - focused */,
                    "primary-content":
                        "#EBF5FF" /* Foreground content color to use on primary color */,

                    "secondary": "#BED2DC" /* Secondary color */,
                    "secondary-focus":
                        "#f3cc30" /* Secondary color - focused */,
                    "secondary-content":
                        "#ffffff" /* Foreground content color to use on secondary color */,

                    "accent": "#37cdbe" /* Accent color */,
                    "accent-focus": "#2aa79b" /* Accent color - focused */,
                    "accent-content":
                        "#ffffff" /* Foreground content color to use on accent color */,

                    "neutral": "#3d4451" /* Neutral color */,
                    "neutral-focus": "#2a2e37" /* Neutral color - focused */,
                    "neutral-content":
                        "#ffffff" /* Foreground content color to use on neutral color */,

                    "base-100":
                        "#ffffff" /* Base color of page, used for blank backgrounds */,
                    "base-200": "#f9fafb" /* Base color, a little darker */,
                    "base-300": "#d1d5db" /* Base color, even more darker */,
                    "base-content":
                        "#1f2937" /* Foreground content color to use on base color */,

                    "info": "#2094f3" /* Info */,
                    "success": "#009485" /* Success */,
                    "warning": "#ff9900" /* Warning */,
                    "error": "#ff5724" /* Error */,
                },
            },
        ],
    },
};
