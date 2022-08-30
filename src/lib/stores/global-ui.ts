import { browser } from "$app/env";
import { get, writable } from "svelte/store";
import type {
    DestructiveOverlayState,
    DestructiveOverlayType,
    DestructiveOverlayAction,
} from "$lib/types";

export const isDarkMode = writable<boolean | null>(null);

function setThemeToNode(node: HTMLElement, dark: boolean): void {
    node.setAttribute("data-theme", dark ? "app-dark" : "app-light");
    if (dark) {
        node.classList.add("dark");
    } else {
        node.classList.remove("dark");
    }
}

const localsThemeKey = "theme";

function systemPreferenceIsDarkMode(): boolean {
    const matchMedia = window.matchMedia("(prefers-color-scheme: dark)");
    return matchMedia.matches;
}

if (browser) {
    if (window.matchMedia) {
        const matchMedia = window.matchMedia("(prefers-color-scheme: dark)");

        const localTheme = localStorage.getItem(localsThemeKey);

        if (localTheme === null) {
            isDarkMode.set(matchMedia.matches);
        } else {
            isDarkMode.set(localTheme == "dark");
        }

        matchMedia.addEventListener("change", (e) => {
            const dark = get(isDarkMode);
            if (dark == null) {
                setThemeToNode(document.body, e.matches);
            }
        });
    }

    window.addEventListener("storage", (event) => {
        if (event.key === localsThemeKey) {
            const localTheme = event.newValue;
            isDarkMode.set(localTheme == "dark");
        }
    });

    isDarkMode.subscribe((value) => {
        console.log("isDarkMode", value);

        if (value == null) {
            value = systemPreferenceIsDarkMode();
        }

        setThemeToNode(document.body, value);
    });
}

export function saveDarkMode(value: boolean | null): void {
    if (value === null) {
        localStorage.removeItem(localsThemeKey);
    } else {
        localStorage.setItem(localsThemeKey, value ? "dark" : "light");
    }
    isDarkMode.set(value);
}

export const destructiveOverlayState = writable<DestructiveOverlayState>({
    kind: "hidden",
});

export function openDestructiveOverlay(
    target: DestructiveOverlayType,
    action: DestructiveOverlayAction
) {
    destructiveOverlayState.update(($destructiveOverlayState) => {
        if ($destructiveOverlayState.kind !== "hidden") {
            throw new Error(
                "Expected $destructiveOverlayState.kind to be hidden"
            );
        }
        return {
            kind: "visible",
            target,
            action,
        };
    });
}

export function closeDestructiveOverlay() {
    destructiveOverlayState.update(($destructiveOverlayState) => {
        if ($destructiveOverlayState.kind !== "visible") {
            throw new Error(
                "Expected $destructiveOverlayState.kind to be visible"
            );
        }
        return {
            kind: "hidden",
        };
    });
}

export function performDestructiveOverlay() {
    destructiveOverlayState.update(($destructiveOverlayState) => {
        if ($destructiveOverlayState.kind !== "visible") {
            throw new Error(
                "Expected $destructiveOverlayState.kind to be visible"
            );
        }
        if ($destructiveOverlayState.action.kind === "sync") {
            $destructiveOverlayState.action.action();
            return { kind: "hidden" };
        } else {
            (async () => {
                await $destructiveOverlayState.action.action();
                destructiveOverlayState.set({
                    kind: "hidden",
                });
            })();
            return $destructiveOverlayState;
        }
    });
}
