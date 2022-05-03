import type { Theme } from "./../components/theme-builder/theme-utils";

import {
    getStyleFor,
    themeToArray,
} from "./../components/theme-builder/theme-utils";

import { browser } from "$app/env";
import { get, writable } from "svelte/store";

export const isDarkMode = writable(false);

function setThemeToNode(node: HTMLElement, dark): void {
    node.setAttribute("data-theme", dark ? "app-dark" : "app-light");
}

const localsThemeKey = "theme";

isDarkMode.subscribe((value) => {
    console.log(value);
    if (browser) {
        localStorage.setItem(localsThemeKey, value ? "dark" : "light");
        setThemeToNode(document.body, value);
    }
});

if (browser) {
    if (window.matchMedia) {
        const matchMedia = window.matchMedia("(prefers-color-scheme: dark)");

        const localThemeIsSet = localStorage.getItem(localsThemeKey) !== null;

        if (!localThemeIsSet) {
            isDarkMode.set(matchMedia.matches);
        }

        matchMedia.addEventListener("change", (e) => {
            isDarkMode.set(e.matches);
        });
    }
}

export type UserTheme = {
    light?: Theme;
    dark?: Theme;
};

export const userTheme = writable<UserTheme>(null);

export function setUserThemeFor(theme: Theme, isDarkMode: boolean): void {
    let ut = get(userTheme);

    if (!ut) {
        ut = {};
    }

    if (isDarkMode) {
        ut.dark = theme;
    } else {
        ut.light = theme;
    }

    userTheme.set(ut);
}

export function getUserThemeFor(isDarkMode: boolean): Theme {
    const themes = get(userTheme);
    return themes && themes[isDarkMode ? "dark" : "light"];
}

export function applyStyleToBody(themes: UserTheme): void {
    if (!browser) {
        return;
    }
    const dm = get(isDarkMode);
    if (!dm) {
        return;
    }
    if (!themes) {
        return;
    }
    const curTheme = themes[dm ? "dark" : "light"];
    const themeArray = themeToArray(curTheme);
    if (!themeArray) {
        return;
    }
    const styles = getStyleFor(themeArray);
    document.body.setAttribute("style", styles);
}

if (browser) {
    const userThemeKey = "userTheme";

    const themeStr = localStorage.getItem(userThemeKey);
    if (themeStr) {
        const theme = JSON.parse(themeStr) as UserTheme;
        userTheme.set(theme);
    }

    window.addEventListener("storage", (event) => {
        if (event.key === userThemeKey) {
            const themes = JSON.parse(event.newValue as string) as UserTheme;
            userTheme.set(themes);
            applyStyleToBody(themes);
        }
    });

    userTheme.subscribe((themes) => {
        const themeStr = JSON.stringify(themes);
        localStorage.setItem(userThemeKey, themeStr);
        applyStyleToBody(themes);
    });
}
