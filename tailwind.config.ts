import type { Config } from "tailwindcss";

// Conflicting color name resolutions
const conflictColors = {
    "foreground": "#FFFFFF",
    "base-TODO": "#FFFFFF",
};
// These are the new colors added 2022-08-04
// Some of them I have marked them as "renamed" in the colors object
const missingColors = {
    // "base": "#FFFFFF", // This conflicts with the font size declaration text-base
    "utility": "#64748B",
    "task-default": "#FFFFFF",
    "task-hover": "#F8FAFC",
    "task-pressed": "#F1F5F9",
    "tertiary-content": "#2563EB",
    "tertiary-content-hover": "#1E3A8A",
    "tertiary-hover": "#DBEAFE",
    "tertiary-pressed": "#93C5FD",
    "disabled-primary-content": "#475569",
    "disabled": "#E2E8F0",
    "disabled-content": "#CBD5E1",
    "destructive-secondary-hover": "#FEE2E2",
    "destructive-secondary-pressed": "#FCA5A5",
    "border-secondary": "#2563EB",
    "border-focus": "#1E293B",
};
const colors = {
    "accent": "#FEE2E2", // unused, renamed to destructive (already in colors)
    "accent-content": "#B91C1C", // unused, renamed to destructive-content (already in colors)
    "accent-content-hover": "#FFFFFF", // unused, but not found in Colors spreadsheet
    "accent-focus": "#FECACA", // unused, renamed to destructive-hover (already in colors)
    "background": "#EFF6FF", // new
    "base-100": "#FFFFFF", // unused, renamed to base (in missingColors)
    "base-200": "#EFF6FF", // unused, renamed to background (already in colors)
    "base-300": "#CBD5E1", // unused, but not found in Colors spreadsheet
    "base-content": "#1E293B", // kept in new Colors spreadsheet
    "border": "#CBD5E1", // new
    "destructive": "#DC2626", // new
    "destructive-content": "#FFFFFF", // new
    "destructive-content-secondary": "#DC2626", // new, but not found in Colors spreadsheet
    "destructive-hover": "#991B1B", // new
    "destructive-pressed": "#7F1D1D", // new
    "destructive-pressed-secondary": "#FCA5A5", // renamed to destructive-secondary-pressed (in missingColors)
    "destructive-secondary": "#FEE2E2", // renamed to destructive-secondary-hover (in missingColors)
    "disabled-background": "#E2E8F0", // renamed to disabled (in missingColors)
    "disabled-text": "#475569", // new, but not found in Colors spreadsheet
    "display": "#FFFFFF", // new, but not found in Colors spreadsheet
    "error": "#EF4444", // keep
    "info": "#0EA5E9", // keep
    "label-blue": "#C8E1FF", // keep
    "label-green": "#CFF0D7", // keep
    "label-hover-blue": "#A0C2EC", // keep
    "label-hover-green": "#ADD7B7", // keep
    "label-hover-orange": "#FED7AA", // keep
    "label-hover-pink": "#EEB0D5", // keep
    "label-hover-purple": "#C3B2EC", // keep
    "label-hover-red": "#F0B0B7", // keep
    "label-hover-yellow": "#E7DC8E", // keep
    "label-orange": "#FFEBDA", // keep
    "label-pink": "#FEDBF0", // keep
    "label-purple": "#DDD6FE", // keep
    "label-red": "#FFDCE0", // keep
    "label-text-blue": "#1E40AF", // renamed
    "label-text-green": "#166534", // renamed
    "label-text-orange": "#9A3412", // renamed
    "label-text-pink": "#9D174D", // renamed
    "label-text-purple": "#5B21B6", // renamed
    "label-text-red": "#991B1B", // renamed
    "label-text-yellow": "#854D0E", // renamed
    "label-yellow": "#FFF5B1", // keep
    "primary": "#2563EB", // keep
    "primary-content": "#ffffff", // keep
    "primary-focus": "#0077FF", // unused, renamed to primary-hover (already in colors)
    "primary-hover": "#1E40AF", // new
    "primary-pressed": "#1E3A8A", // new
    "secondary": "#2563EB", // unused, renamed to secondary-hover (already in colors)
    "secondary-content": "#2563EB", // keep
    "secondary-content-hover": "#1E40AF", // new
    "secondary-focus": "#93C5FD", // unused, rename to secondary-pressed (already in colors)
    "secondary-hover": "#DBEAFE", // new
    "secondary-pressed": "#93C5FD", // new
    "secondary-text": "#8390A2", // unused, but not found in Colors spreadsheet
    "secondary-text-hover": "#64748B", // unused, but not found in Colors spreadsheet
    "success": "#0D9488", // keep
    "task-bg-default": "#FFFFFF", // unused, but not found in Colors spreadsheet
    "task-bg-hover": "#F8FAFC", // unused, but not found in Colors spreadsheet
    "task-bg-pressed": "#F1F5F9", // unused, but not found in Colors spreadsheet
    "warning": "#F59E0B", // keep
    ...missingColors,
    ...conflictColors,
};

const config: Config = {
    darkmode: "class",
    mode: "jit",
    content: ["./src/**/*.{json,html,js,svelte,ts}"],
    theme: {
        extend: {
            fontFamily: {
                sans: ["Roboto", "sans-serif"],
            },
            fontSize: {
                xxs: "10px",
            },
            borderRadius: {
                "llg": "10px",
                "1.5xl": "14px",
                "2.5xl": "20px",
            },
            boxShadow: {
                "card": "0px 0px 4px 0px #1E202940",
                "sm": "0 1px 2px rgba(0, 0, 0, 0.15)",
                "lg": "0 2px 8px rgba(0, 0, 0, 0.25)",
                "xl": "0 4px 16px rgba(0, 0, 0, 0.15)",
                "context-menu": "1px 4px 8px rgba(0, 0, 0, 0.25)",
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
    plugins: [require("@tailwindcss/typography")],
};
export default config;
