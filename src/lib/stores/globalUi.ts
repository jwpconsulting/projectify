import type { Writable } from "svelte/store";
import type {
    ConstructiveOverlayState,
    ConstructiveOverlayType,
    ContextMenuState,
    ContextMenuType,
    DestructiveOverlayState,
    DestructiveOverlayType,
    Overlay,
    OverlayAction,
} from "$lib/types/ui";
import { internallyWritable } from "$lib/stores/util";

const { priv: _constructiveOverlayState, pub: constructiveOverlayState } =
    internallyWritable<ConstructiveOverlayState>({
        kind: "hidden",
    });
export { constructiveOverlayState };

const { priv: _destructiveOverlayState, pub: destructiveOverlayState } =
    internallyWritable<DestructiveOverlayState>({
        kind: "hidden",
    });
export { destructiveOverlayState };

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
    openOverlay(_destructiveOverlayState, target, action);
}

export function closeDestructiveOverlay() {
    closeOverlay(_destructiveOverlayState);
}

export function performDestructiveOverlay() {
    _destructiveOverlayState.update(($destructiveOverlayState) => {
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
                _destructiveOverlayState.set({
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
    openOverlay(_constructiveOverlayState, target, action);
}

export function closeConstructiveOverlay() {
    closeOverlay(_constructiveOverlayState);
}

const { priv: _contextMenuState, pub: contextMenuState } =
    internallyWritable<ContextMenuState>({
        kind: "hidden",
    });
export { contextMenuState };
export function openContextMenu(target: ContextMenuType, anchor: HTMLElement) {
    _contextMenuState.update(($contextMenuState) => {
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
    _contextMenuState.update(($contextMenuState) => {
        if ($contextMenuState.kind === "hidden") {
            throw new Error("Expected $contextMenuState.kind to be visible");
        }
        return {
            kind: "hidden",
        };
    });
}
