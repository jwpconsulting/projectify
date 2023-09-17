<script lang="ts">
    import { onMount } from "svelte";

    import { browser } from "$app/environment";
    import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
    import {
        closeContextMenu,
        contextMenuState,
        handleKey,
    } from "$lib/stores/globalUi";
    import type { ContextMenuState } from "$lib/types/ui";
    import { keepFocusInside } from "$lib/utils/focus";

    let contextMenu: HTMLElement | null = null;
    let resizeObserver: ResizeObserver | null = null;
    let repositioned = false;

    onMount(() => {
        if (!browser) {
            return undefined;
        }

        let unfocus: undefined | (() => void) = undefined;
        let escapeUnsubscriber: (() => void) | undefined = undefined;
        const unsubscriber = contextMenuState.subscribe(
            ($contextMenuState) => {
                if (!contextMenu) {
                    throw new Error("Expected contextMenu");
                }
                if ($contextMenuState.kind === "visible") {
                    if (resizeObserver) {
                        throw new Error("There already was a resizeObserver");
                    }
                    unfocus = keepFocusInside(contextMenu);
                    addObserver(contextMenu, $contextMenuState);
                    escapeUnsubscriber = handleKey("Escape", closeContextMenu);
                } else {
                    if (unfocus) {
                        unfocus();
                        unfocus = undefined;
                    }
                    resizeObserver = null;
                    repositioned = false;
                    if (escapeUnsubscriber) {
                        escapeUnsubscriber();
                        escapeUnsubscriber = undefined;
                    }
                }
            }
        );
        return () => {
            // It follows that when a context menu is visible, there is a focus
            // lock. Might be a good chance to do an integrity check here.
            if (unfocus) {
                unfocus();
                unfocus = undefined;
            }
            unsubscriber();
            // Think about whether this one is necessary
            closeContextMenu();
            if (escapeUnsubscriber) {
                escapeUnsubscriber();
                escapeUnsubscriber = undefined;
            }
        };
    });

    function addObserver(
        contextMenu: HTMLElement,
        $contextMenuState: ContextMenuState & { kind: "visible" }
    ) {
        console.debug($contextMenuState);
        const anchor = $contextMenuState.anchor;
        repositioned = false;
        resizeObserver = new ResizeObserver(() =>
            repositionContextMenu(anchor)
        );
        resizeObserver.observe(contextMenu);
    }

    function repositionContextMenu(anchor: HTMLElement) {
        if (!contextMenu) {
            throw new Error("Expected contextMenu");
        }
        if (repositioned) {
            console.debug("already repositioned");
            return;
        }
        if (contextMenu.offsetWidth == 0) {
            console.debug("waiting for contextMenu to grow");
            return;
        }
        console.debug("repositioning");
        const rect = anchor.getBoundingClientRect();
        const anchorLeft = rect.left;
        const anchorTop = rect.top;
        // Get width of viewport
        const viewPortWidth = document.body.clientWidth;
        // Get x of right side of context menu
        const xRightSide = anchorLeft + contextMenu.offsetWidth;
        // Calculate how many pixels the right side of contextMenu will go
        // over the width
        const xOverlap = Math.max(0, xRightSide - viewPortWidth);
        console.debug("offsetWidth", contextMenu.offsetWidth);
        console.debug({ viewPortWidth, anchorLeft, xRightSide, xOverlap });
        if (xOverlap > 0) {
            console.debug("xOverlap", xOverlap);
        }
        // Subtract the overlapy from y
        const x = anchorLeft - xOverlap;
        // Get height of viewport
        const viewPortHeight = document.body.clientHeight;
        // Calculate how many pixels from anchor bottom to viewport bottom
        const anchorBottomToViewPortBottom = Math.abs(
            viewPortHeight - (anchorTop + anchor.offsetHeight)
        );
        // Calculate how many pixels high the context menu is
        const contextMenuHeight = contextMenu.offsetHeight;
        let y: number;
        // If the context menu takes up more pixels, then reposition the context
        // menu to be above the anchor
        if (contextMenuHeight > anchorBottomToViewPortBottom)
            // Subtract the overlap from y
            y = rect.top - contextMenuHeight;
        else {
            // Else position it under the anchor;
            y = rect.top + anchor.offsetHeight;
        }

        contextMenu.style.left = `${x}px`;
        contextMenu.style.top = `${y}px`;

        if (!resizeObserver) {
            throw new Error("Expected resizeObserver");
        }
        resizeObserver.disconnect();
        repositioned = true;
    }
</script>

<button
    class="bg-red fixed left-0 top-0 h-full w-full"
    class:hidden={$contextMenuState.kind === "hidden"}
    on:click={closeContextMenu}
    on:keydown={closeContextMenu}
/>
<div
    class:fixed={$contextMenuState.kind === "visible"}
    class:hidden={$contextMenuState.kind === "hidden"}
    bind:this={contextMenu}
>
    {#if $contextMenuState.kind === "visible"}
        <ContextMenu target={$contextMenuState.target} />
    {/if}
</div>
