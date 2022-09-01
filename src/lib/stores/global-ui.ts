import { writable } from "svelte/store";
import type {
    DestructiveOverlayState,
    DestructiveOverlayType,
    DestructiveOverlayAction,
} from "$lib/types";

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
