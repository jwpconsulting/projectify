const factoryLightThemeColors = {};

const factoryDarkThemeColors = {};

const commonTheme = {
    "fontFamily": "Roboto, sans-serif",
    "--btn-text-case": "none",
};
const colors = {
    "accent": "#FEE2E2", // unused
    "accent-content": "#B91C1C", // unused
    "accent-content-hover": "#FFFFFF",
    "accent-focus": "#FECACA", // unused
    "background": "#EFF6FF",
    "base-100": "#FFFFFF", // unused
    "base-200": "#EFF6FF", // unused
    "base-300": "#CBD5E1", // unused
    "base-content": "#1E293B",
    "border": "#CBD5E1",
    "destructive": "#DC2626",
    "destructive-content": "#FFFFFF",
    "destructive-content-secondary": "#DC2626",
    "destructive-hover": "#991B1B",
    "destructive-pressed": "#7F1D1D",
    "destructive-pressed-secondary": "#FCA5A5",
    "destructive-secondary": "#FEE2E2",
    "disabled-background": "#E2E8F0",
    "disabled-text": "#475569",
    "display": "#FFFFFF",
    "error": "#EF4444",
    "info": "#0EA5E9",
    "label-blue": "#C8E1FF",
    "label-green": "#CFF0D7",
    "label-hover-blue": "#A0C2EC",
    "label-hover-green": "#ADD7B7",
    "label-hover-orange": "#FED7AA",
    "label-hover-pink": "#EEB0D5",
    "label-hover-purple": "#C3B2EC",
    "label-hover-red": "#F0B0B7",
    "label-hover-yellow": "#E7DC8E",
    "label-orange": "#FFEBDA",
    "label-pink": "#FEDBF0",
    "label-purple": "#DDD6FE",
    "label-red": "#FFDCE0",
    "label-text-blue": "#1E40AF",
    "label-text-green": "#166534",
    "label-text-orange": "#9A3412",
    "label-text-pink": "#9D174D",
    "label-text-purple": "#5B21B6",
    "label-text-red": "#991B1B",
    "label-text-yellow": "#854D0E",
    "label-yellow": "#FFF5B1",
    "primary": "#2563EB",
    "primary-content": "#ffffff",
    "primary-focus": "#0077FF", // unused
    "primary-hover": "#1E40AF",
    "primary-pressed": "#1E40AF",
    "secondary": "#DBEAFE", // unused
    "secondary-content": "#FFFFFF",
    "secondary-content-hover": "#1E40AF",
    "secondary-focus": "#93C5FD", // unused
    "secondary-hover": "#DBEAFE",
    "secondary-pressed": "#93C5FD",
    "secondary-text": "#8390A2",
    "secondary-text-hover": "#64748B",
    "success": "#0D9488",
    "task-bg-default": "#FFFFFF",
    "task-bg-hover": "#F8FAFC",
    "task-bg-pressed": "#F1F5F9",
    "warning": "#F59E0B",
};

module.exports = {
    darkmode: "class",
    mode: "jit",
    content: ["./src/**/*.{json,html,js,svelte,ts}"],
    theme: {
        extend: {
            fontFamily: {
                Rampart: ["Roboto", "sans-serif"],
            },
            fontSize: {
                xxs: "0.625rem",
            },
            borderRadius: {
                "llg": "10px",
                "2.5xl": "20px",
            },
            boxShadow: {
                card: "0px 0px 4px 0px #1E202940",
                sm: "0 1px 2px rgba(0, 0, 0, 0.15)",
                lg: "0 2px 8px rgba(0, 0, 0, 0.25)",
                xl: "0 4px 16px rgba(0, 0, 0, 0.15)",
            },
            colors: colors,
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
    ],
};
