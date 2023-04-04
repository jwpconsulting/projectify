import type { Writable } from "svelte/store";
import { writable } from "svelte/store";
import type {
    ConstructiveOverlayState,
    ConstructiveOverlayType,
    DestructiveOverlayState,
    DestructiveOverlayType,
    OverlayAction,
    ContextMenuType,
    ContextMenuState,
    Overlay,
} from "$lib/types/ui";

// TODO make readonly
export const constructiveOverlayState = writable<ConstructiveOverlayState>({
    kind: "hidden",
});

export const destructiveOverlayState = writable<DestructiveOverlayState>({
    kind: "hidden",
});

function openOverlay<Target, Action>(
    overlay: Writable<Overlay<Target, Action>>,
    target: Target,
    action: Action
) {
    overlay.update(($overlay) => {
        if ($overlay.kind !== "hidden") {
            throw new Error("Expected $overlay.kind to be hidden");
        }
        return {
            kind: "visible",
            target,
            action,
        };
    });
}

function closeOverlay(overlay: Writable<Overlay<unknown, unknown>>) {
    overlay.update(($overlay) => {
        if ($overlay.kind !== "visible") {
            throw new Error("Expected $overlay.kind to be visible");
        }
        return {
            kind: "hidden",
        };
    });
}

export function openDestructiveOverlay(
    target: DestructiveOverlayType,
    action: OverlayAction
) {
    openOverlay(destructiveOverlayState, target, action);
}

export function closeDestructiveOverlay() {
    closeOverlay(destructiveOverlayState);
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

export function openConstructiveOverlay(
    target: ConstructiveOverlayType,
    action: OverlayAction
) {
    openOverlay(constructiveOverlayState, target, action);
}

export function closeConstructiveOverlay() {
    closeOverlay(constructiveOverlayState);
}

export const contextMenuState = writable<ContextMenuState>({
    kind: "hidden",
});
export function openContextMenu(target: ContextMenuType, anchor: HTMLElement) {
    contextMenuState.update(($contextMenuState) => {
        if ($contextMenuState.kind !== "hidden") {
            throw new Error("Expected $contextMenuState.kind to be hidden");
        }
        return {
            kind: "visible",
            target,
            anchor,
        };
    });
}
export function closeContextMenu() {
    contextMenuState.update(($contextMenuState) => {
        if ($contextMenuState.kind === "hidden") {
            throw new Error("Expected $contextMenuState.kind to be visible");
        }
        return {
            kind: "hidden",
        };
    });
}
