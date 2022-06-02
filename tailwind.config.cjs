const factoryLightThemeColors = {
    "primary": "#288CFF",
    "primary-focus": "#0077FF",
    "primary-content": "#ffffff",
    "secondary": "#BEDCFF",
    "secondary-focus": "#76B4F9",
    "secondary-content": "#ffffff",
    "accent": "#EF7D69",
    "accent-focus": "#F05F46",
    "accent-content": "#ffffff",
    "neutral": "#3578C0",
    "neutral-focus": "#5399E4",
    "neutral-content": "#ffffff",
    "base-100": "#ffffff",
    "base-200": "#F2F8FF",
    "base-300": "#d1d5db",
    "base-content": "#1f2937",
    "info": "#2094f3",
    "success": "#009485",
    "warning": "#ff9900",
    "error": "#ff5724",
};

const factoryDarkThemeColors = {
    "primary": "#288CFF",
    "primary-focus": "#0077FF",
    "primary-content": "#ffffff",
    "secondary": "#BEDCFF",
    "secondary-focus": "#76B4F9",
    "secondary-content": "#333333",
    "accent": "#EF7D69",
    "accent-focus": "#F05F46",
    "accent-content": "#ffffff",
    "neutral": "#5B5AA0",
    "neutral-focus": "#7F7ED3",
    "neutral-content": "#ffffff",
    "base-100": "#282841",
    "base-200": "#191e32",
    "base-300": "#3c3c5a",
    "base-content": "#ffffff",
    "info": "#2094f3",
    "success": "#009485",
    "warning": "#ff9900",
    "error": "#ff5724",
};

module.exports = {
    darkMode: "class",
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
        darkTheme: "app-dark",
        themes: [{
                "app-light": {
                    fontFamily: "Roboto, sans-serif",
                    ...factoryLightThemeColors,
                },
            },
            {
                "app-dark": {
                    fontFamily: "Roboto, sans-serif",
                    ...factoryDarkThemeColors,
                },
            },
        ],
    },
};
