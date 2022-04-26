import { browser } from "$app/env";
import { writable } from "svelte/store";
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

// export function checkUserPrefersColorScheme(): void {
//     if (
//         localStorage.theme === "dark" ||
//         (!("theme" in localStorage) &&
//             window.matchMedia("(prefers-color-scheme: dark)").matches)
//     ) {
//         document.documentElement.classList.add("dark");
//     } else {
//         document.documentElement.classList.remove("dark");
//     }
// }
