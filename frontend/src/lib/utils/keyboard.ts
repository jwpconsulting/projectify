// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK

type KeyCallback = (e: KeyboardEvent) => void;
// Let's whitelist keys we'd like to handle for now
type KeyboardKey = "Escape" | "Enter" | "j" | "k" | "h" | "l";

// Decorate a callback and only pass on events when we match the specified
// key
function filterKey(key: KeyboardKey, fn: KeyCallback) {
    return (e: KeyboardEvent) => {
        if (document.activeElement?.nodeName === "INPUT") {
            return;
        }
        if (e.key !== key) {
            return;
        }
        fn(e);
    };
}

export function handleKey(
    key: KeyboardKey,
    callback: KeyCallback,
): () => void {
    const listener = filterKey(key, callback);
    document.addEventListener("keydown", listener);
    return () => document.removeEventListener("keydown", listener);
}
