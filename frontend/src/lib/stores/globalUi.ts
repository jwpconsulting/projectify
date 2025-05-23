// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import type { Writable } from "svelte/store";

import { internallyWritable } from "$lib/stores/util";
import type {
    ConstructiveOverlayState,
    ConstructiveOverlayType,
    ContextMenuState,
    ContextMenuType,
    DestructiveOverlayState,
    DestructiveOverlayType,
    MobileMenuState,
    MobileMenuType,
    Overlay,
    OverlaySuccess,
} from "$lib/types/ui";

const closedState = { kind: "hidden" as const };

const { priv: _constructiveOverlayState, pub: constructiveOverlayState } =
    internallyWritable<ConstructiveOverlayState>(closedState);
export { constructiveOverlayState };

const { priv: _destructiveOverlayState, pub: destructiveOverlayState } =
    internallyWritable<DestructiveOverlayState>(closedState);
export { destructiveOverlayState };

const { priv: _mobileMenuState, pub: mobileMenuState } =
    internallyWritable<MobileMenuState>(closedState);
export { mobileMenuState };

function makeOpenState<Target>(
    target: Target,
    resolve: () => void,
    reject: () => void,
): Overlay<Target> {
    return {
        kind: "visible",
        target,
        resolve,
        reject,
    };
}

async function openOverlay<Target>(
    overlay: Writable<Overlay<Target>>,
    target: Target,
    expectHidden = true,
): Promise<void> {
    return await new Promise((resolve: () => void, reject: () => void) => {
        overlay.update(($overlay) => {
            if ($overlay.kind !== "hidden") {
                if (expectHidden) {
                    throw new Error("Expected $overlay.kind to be hidden");
                } else {
                    console.debug(
                        "Tried to open overlay",
                        overlay,
                        ", but it was already visible with",
                        target,
                    );
                }
            }
            return makeOpenState(target, resolve, reject);
        });
    });
}

function closeOverlay(
    overlay: Writable<Overlay<unknown>>,
    success: OverlaySuccess,
    expectVisible = true,
) {
    overlay.update(($overlay) => {
        if ($overlay.kind !== "visible") {
            if (expectVisible) {
                throw new Error("Expected $overlay.kind to be visible");
            } else {
                console.debug("Tried to close overlay, but it wasn't visible");
                return $overlay;
            }
        }
        if (success == "success") {
            $overlay.resolve();
        } else {
            $overlay.reject(new Error("Overlay was cancelled"));
        }
        return closedState;
    });
}

async function toggleOverlay<Target>(
    overlay: Writable<Overlay<Target>>,
    target: Target,
): Promise<void> {
    return await new Promise((resolve: () => void, reject: () => void) => {
        overlay.update(($overlay) => {
            if ($overlay.kind === "hidden") {
                return makeOpenState(target, resolve, reject);
            } else {
                // If we resolve immediately like this, we might want to
                // have another status than "success"
                resolve();
                return closedState;
            }
        });
    });
}

export async function openDestructiveOverlay(
    target: DestructiveOverlayType,
): Promise<void> {
    return await openOverlay(_destructiveOverlayState, target);
}

// call only when failed
export function rejectDestructiveOverlay() {
    closeOverlay(_destructiveOverlayState, "rejected");
}

export function resolveDestructiveOverlay() {
    closeOverlay(_destructiveOverlayState, "success");
}

export async function openConstructiveOverlay(
    target: ConstructiveOverlayType,
): Promise<void> {
    return openOverlay(_constructiveOverlayState, target);
}

export function rejectConstructiveOverlay() {
    closeOverlay(_constructiveOverlayState, "rejected");
}

export function resolveConstructiveOverlay() {
    closeOverlay(_constructiveOverlayState, "success");
}

export function closeMobileMenu() {
    closeOverlay(_mobileMenuState, "success", false);
}

export async function toggleMobileMenu(type: MobileMenuType) {
    await toggleOverlay(_mobileMenuState, type);
}

const { priv: _contextMenuState, pub: contextMenuState } =
    internallyWritable<ContextMenuState>({
        kind: "hidden",
    });
export { contextMenuState };
export async function openContextMenu(
    target: ContextMenuType,
    anchor: HTMLElement,
): Promise<void> {
    return await new Promise((resolve, reject) => {
        _contextMenuState.update(($contextMenuState) => {
            if ($contextMenuState.kind !== "hidden") {
                // Context menus don't have any callback they need to resolve,
                // so we can safely reopen it somewhere else and not degrade UX
                console.warn(
                    "Context menu was already visible, changing target and anchor",
                    target,
                    anchor,
                );
            }
            return {
                kind: "visible",
                target,
                anchor,
                resolve,
                reject,
            };
        });
    });
}

export function closeContextMenu() {
    closeOverlay(_contextMenuState, "success", false);
}
