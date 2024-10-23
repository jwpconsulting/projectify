// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Listen to scroll events, call callback, return unsubscriber
 */
export function onScroll(callback: () => void): () => void {
    document.addEventListener("scroll", callback);
    return () => document.removeEventListener("scroll", callback);
}
