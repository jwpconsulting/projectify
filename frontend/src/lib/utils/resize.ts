// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Call a callback on every window resize until this function's return value
 * is called
 */
export function onResize(callback: () => void): () => void {
    addEventListener("resize", callback);
    return () => removeEventListener("resize", callback);
}
