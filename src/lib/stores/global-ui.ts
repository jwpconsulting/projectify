import type { Theme } from "./../components/theme-builder/theme-utils";
import { browser } from "$app/env";
import { get, writable } from "svelte/store";

export const isDarkMode = writable(false);

function setThemeToNode(node: HTMLElement, dark): void {
    node.setAttribute("data-theme", dark ? "app-dark" : "app-light");
}

isDarkMode.subscribe((value) => {
    console.log(value);
    if (browser) {
        localStorage.setItem("theme", value ? "dark" : "light");
        setThemeToNode(document.body, value);
    }
});

if (browser) {
    if (window.matchMedia) {
        const matchMedia = window.matchMedia("(prefers-color-scheme: dark)");
        isDarkMode.set(matchMedia.matches);
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

// const applyCustomThemeEnabled = true;

if (browser) {
    const userThemeKey = "userTheme";

    const themeStr = localStorage.getItem(userThemeKey);
    if (themeStr) {
        const theme = JSON.parse(themeStr) as UserTheme;
        userTheme.set(theme);
    }

    window.addEventListener("storage", (event) => {
        if (event.key === userThemeKey) {
            const theme = JSON.parse(event.newValue as string) as UserTheme;
            userTheme.set(theme);
        }
    });

    userTheme.subscribe((themes) => {
        const themeStr = JSON.stringify(themes);
        localStorage.setItem(userThemeKey, themeStr);

        // if (browser && applyCustomThemeEnabled) {
        //     const dm = get(isDarkMode);
        //     const curTheme = themes[isDarkMode ? "dark" : "light"];
        //     if (curTheme) {
        //         console.log("curTheme", curTheme);
        //     }
        //     // document.body.
        // }
    });
}
