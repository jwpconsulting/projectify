const factoryLightThemeColors = {};

const factoryDarkThemeColors = {};

const commonTheme = {
    "fontFamily": "Roboto, sans-serif",
    "--btn-text-case": "none",
    "primary": "#3B82F6",
    "primary-focus": "#0077FF",
    "primary-content": "#ffffff",
    "secondary": "#DBEAFE",
    "secondary-focus": "#93C5FD",
    "secondary-content": "#FFFFFF",
    "accent": "#FEE2E2",
    "accent-focus": "#FECACA",
    "accent-content": "#B91C1C",
    "base-100": "#FFFFFF",
    "base-200": "#EFF6FF",
    "base-300": "#CBD5E1",
    "base-content": "#1E293B",
    "info": "#0EA5E9",
    "success": "#0D9488",
    "warning": "#F59E0B",
    "error": "#EF4444",
};

module.exports = {
    darkmode: "class",
    mode: "jit",
    content: ["./src/**/*.{json,html,js,svelte,ts}"],
    theme: {
        colors: {
            "primary-content-hover": "#2563EB",
            "secondary-content-hover": "#93C5FD",
            "accent-content-hover": "#FFFFFF",
            "disabled-text": "#64748B",
            "disabled-background": "#E2E8F0",
            "secondary-text": "#8390A2",
            "secondary-text-hover": "#64748B",
            "label-orange": "#FFEBDA",
            "label-pink": "#FEDBF0",
            "label-blue": "#C8E1FF",
            "label-purple": "#DDD6FE",
            "label-yellow": "#FFF5B1",
            "label-red": "#FFDCE0",
            "label-green": "#CFF0D7",
            "label-hover-orange": "#FED7AA",
            "label-hover-pink": "#EEB0D5",
            "label-hover-blue": "#A0C2EC",
            "label-hover-purple": "#C3B2EC",
            "label-hover-yellow": "#E7DC8E",
            "label-hover-red": "#F0B0B7",
            "label-hover-green": "#ADD7B7",
            "label-text-orange": "#9A3412",
            "label-text-pink": "#9D174D",
            "label-text-blue": "#1E40AF",
            "label-text-purple": "#5B21B6",
            "label-text-yellow": "#854D0E",
            "label-text-red": "#991B1B",
            "label-text-green": "#166534",
        },
        extend: {
            fontFamily: {
                Rampart: ["Roboto", "sans-serif"],
            },
            fontSize: {
                xxs: "0.625rem",
            },
            borderRadius: {
                llg: "10px",
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
        require("@tailwindcss/line-clamp"),
        require("daisyui"),
    ],

    daisyui: {
        styled: true,
        darkTheme: "app-dark",
        themes: [
            {
                "app-light": {
                    ...commonTheme,
                    ...factoryLightThemeColors,
                },
            },
            {
                "app-dark": {
                    ...commonTheme,
                    ...factoryDarkThemeColors,
                },
            },
        ],
    },
};
