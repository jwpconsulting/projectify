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
                xl: "0 4px 16px rgba(0, 0, 0, 0.15)",
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
                    "primary": "#288CFF" /* Primary color */,
                    "primary-focus": "#0077FF" /* Primary color - focused */,
                    "primary-content":
                        "#ffffff" /* Foreground content color to use on primary color */,

                    "secondary": "#BEDCFF" /* Secondary color */,
                    "secondary-focus":
                        "#76B4F9" /* Secondary color - focused */,
                    "secondary-content":
                        "#ffffff" /* Foreground content color to use on secondary color */,

                    "accent": "#EF7D69" /* Accent color */,
                    "accent-focus": "#F05F46" /* Accent color - focused */,
                    "accent-content":
                        "#ffffff" /* Foreground content color to use on accent color */,

                    "neutral": "#ffffff" /* Neutral color */,
                    "neutral-focus": "#eeeeee" /* Neutral color - focused */,
                    "neutral-content":
                        "#333333" /* Foreground content color to use on neutral color */,

                    "base-100":
                        "#ffffff" /* Base color of page, used for blank backgrounds */,
                    "base-200": "#F2F8FF" /* Base color, a little darker */,
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
