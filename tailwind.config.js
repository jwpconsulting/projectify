// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/** @typedef {import("tailwindcss").Config} Config */

// Conflicting color name resolutions
const conflictColors = {
    "foreground": "#FFFFFF",
};
// These are the new colors added 2022-08-04
// Some of them I have marked them as "renamed" in the colors object
const missingColors = {
    // "base": "#FFFFFF", // This conflicts with the font size declaration text-base
};
const colors = {
    "background": "#EFF6FF", // new
    "base-content": "#1E293B", // kept in new Colors spreadsheet
    "border": "#CBD5E1", // new
    "border-secondary": "#2563EB",
    "destructive": "#DC2626", // new
    "destructive-content": "#FFFFFF", // new
    "destructive-content-secondary": "#DC2626", // new, but not found in Colors spreadsheet
    "destructive-hover": "#991B1B", // new
    "destructive-pressed": "#7F1D1D", // new
    "destructive-secondary-hover": "#FEE2E2",
    "destructive-secondary-pressed": "#FCA5A5",
    "disabled": "#E2E8F0",
    "disabled-content": "#CBD5E1",
    "disabled-primary-content": "#475569",
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
    "primary-hover": "#1E40AF", // new
    "primary-pressed": "#1E3A8A", // new
    "secondary-content": "#2563EB", // keep
    "secondary-content-hover": "#1E40AF", // new
    "secondary-hover": "#DBEAFE", // new
    "secondary-pressed": "#93C5FD", // new
    "success": "#0D9488", // keep
    "task-default": "#FFFFFF",
    "task-hover": "#F8FAFC",
    "task-pressed": "#F1F5F9",
    "utility": "#64748B",
    "warning": "#F59E0B", // keep
    ...missingColors,
    ...conflictColors,
};

/** @type Config */
const config = {
    darkmode: "class",
    mode: "jit",
    // ../../ is the projectify directory
    content: [
        // Apps and shared templates
        "projectify/**/templates/**/*.html",
        "projectify/**/const.py",
        // Heroicons
        "projectify/templates/heroicons/*.svg",
        // Templatetags
        "projectify/templatetags/*.py",
    ],
    theme: {
        extend: {
            borderRadius: {
                // TODO Check if still needed
                "llg": "10px",
                // TODO Check if still needed
                "1.5xl": "14px",
                // TODO Check if still needed
                "2.5xl": "20px",
            },
            boxShadow: {
                // TODO Check if still needed
                "card": "0px 0px 4px 0px #1E202940",
                // TODO Check if still needed
                "sm": "0 1px 2px rgba(0, 0, 0, 0.15)",
                // TODO Check if still needed
                "lg": "0 2px 8px rgba(0, 0, 0, 0.25)",
                // TODO Check if still needed
                "xl": "0 4px 16px rgba(0, 0, 0, 0.15)",
                // TODO Check if still needed
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
