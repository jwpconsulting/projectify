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
    closeCallback: (success: OverlaySuccess) => void
): Overlay<Target> {
    return {
        kind: "visible",
        target,
        closeCallback,
    };
}

function openOverlay<Target>(
    overlay: Writable<Overlay<Target>>,
    target: Target
) {
    return new Promise<OverlaySuccess>(
        (resolve: (success: OverlaySuccess) => void) => {
            overlay.update(($overlay) => {
                if ($overlay.kind !== "hidden") {
                    throw new Error("Expected $overlay.kind to be hidden");
                }
                return makeOpenState(target, resolve);
            });
        }
    );
}

function closeOverlay(
    overlay: Writable<Overlay<unknown>>,
    success: OverlaySuccess
) {
    overlay.update(($overlay) => {
        if ($overlay.kind !== "visible") {
            throw new Error("Expected $overlay.kind to be visible");
        }
        $overlay.closeCallback(success);
        return closedState;
    });
}

function toggleOverlay<Target>(
    overlay: Writable<Overlay<Target>>,
    target: Target
) {
    return new Promise((resolve: (success: OverlaySuccess) => void) => {
        overlay.update(($overlay) => {
            if ($overlay.kind === "hidden") {
                return makeOpenState(target, resolve);
            } else {
                // If we resolve immediately like this, we might want to
                // have another status than "success"
                resolve("success");
                return closedState;
            }
        });
    });
}

export async function openDestructiveOverlay(
    target: DestructiveOverlayType
): Promise<OverlaySuccess> {
    return openOverlay(_destructiveOverlayState, target);
}

// most likely called when unsuccessful
export function closeDestructiveOverlay() {
    closeOverlay(_destructiveOverlayState, "unknown");
}

export function performDestructiveOverlay() {
    _destructiveOverlayState.update(($destructiveOverlayState) => {
        if ($destructiveOverlayState.kind !== "visible") {
            throw new Error(
                "Expected $destructiveOverlayState.kind to be visible"
            );
        }
        $destructiveOverlayState.closeCallback("success");
        return { kind: "hidden" };
    });
}

export async function openConstructiveOverlay(
    target: ConstructiveOverlayType
): Promise<OverlaySuccess> {
    return openOverlay(_constructiveOverlayState, target);
}

export function closeConstructiveOverlay() {
    closeOverlay(_constructiveOverlayState, "unknown");
}

export function closeMobileMenu() {
    closeOverlay(_mobileMenuState, "unknown");
}

export async function toggleMobileMenu(type: MobileMenuType) {
    await toggleOverlay(_mobileMenuState, type);
}

const { priv: _contextMenuState, pub: contextMenuState } =
    internallyWritable<ContextMenuState>({
        kind: "hidden",
    });
export { contextMenuState };
export function openContextMenu(target: ContextMenuType, anchor: HTMLElement) {
    _contextMenuState.update(($contextMenuState) => {
        if ($contextMenuState.kind !== "hidden") {
            // Context menus don't have any callback they need to resolve,
            // so we can safely reopen it somewhere else and not degrade UX
            console.warn(
                "Context menu was already visible, changing target and anchor",
                target,
                anchor
            );
        }
        return {
            kind: "visible",
            target,
            anchor,
        };
    });
}
export function closeContextMenu() {
    _contextMenuState.update(($contextMenuState) => {
        if ($contextMenuState.kind === "hidden") {
            console.warn("Context menu was already hidden", $contextMenuState);
            return $contextMenuState;
        }
        return {
            kind: "hidden",
        };
    });
}

type KeyCallback = (e: KeyboardEvent) => void;
// Let's whitelist keys we'd like to handle for now
type KeyboardKey = "Escape" | "Enter";

// Decorate a callback and only pass on events when we match the specified
// key
function filterKey(key: KeyboardKey, fn: KeyCallback) {
    return (e: KeyboardEvent) => {
        if (e.key !== key) {
            return;
        }
        fn(e);
    };
}

type Unsubscriber = () => void;

export function handleKey(
    key: KeyboardKey,
    callback: KeyCallback
): Unsubscriber {
    const listener = filterKey(key, callback);
    document.addEventListener("keydown", listener);
    return () => document.removeEventListener("keydown", listener);
}
