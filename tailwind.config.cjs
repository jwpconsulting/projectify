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
                sm: "0 1px 2px rgba(0, 0, 0, 0.15)",
                lg: "0 2px 8px rgba(0, 0, 0, 0.25)",
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
        // require("tailwind-children"),
        require("@tailwindcss/typography"),
        require("daisyui"),
    ],

    daisyui: {
        styled: true,
        themes: [
            {
                "app-light": {
                    "fontFamily": "Roboto, sans-serif",

                    "primary": "#288CFF",
                    "primary-focus": "#0077FF",
                    "primary-content": "#ffffff",
                    "secondary": "#BEDCFF",
                    "secondary-focus": "#76B4F9",
                    "secondary-content": "#ffffff",
                    "accent": "#EF7D69",
                    "accent-focus": "#F05F46",
                    "accent-content": "#ffffff",
                    "neutral": "#ffffff",
                    "neutral-focus": "#eeeeee",
                    "neutral-content": "#333333",
                    "base-100": "#ffffff",
                    "base-200": "#F2F8FF",
                    "base-300": "#d1d5db",
                    "base-content": "#1f2937",
                    "info": "#2094f3",
                    "success": "#009485",
                    "warning": "#ff9900",
                    "error": "#ff5724",
                },

                "app-dark": {
                    "fontFamily": "Roboto, sans-serif",

                    "primary": "#288CFF",
                    "primary-focus": "#0077FF",
                    "primary-content": "#ffffff",
                    "secondary": "#BEDCFF",
                    "secondary-focus": "#76B4F9",
                    "secondary-content": "#ffffff",
                    "accent": "#EF7D69",
                    "accent-focus": "#F05F46",
                    "accent-content": "#ffffff",
                    "neutral": "#ffffff",
                    "neutral-focus": "#eeeeee",
                    "neutral-content": "#333333",
                    "base-100": "#34363a",
                    "base-200": "#202123",
                    "base-300": "#5c5c5c",
                    "base-content": "#ffffff",
                    "info": "#2094f3",
                    "success": "#009485",
                    "warning": "#ff9900",
                    "error": "#ff5724",
                },
            },
        ],
    },
};
