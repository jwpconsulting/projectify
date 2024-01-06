<script lang="ts">
    import { onMount } from "svelte";

    import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
    import {
        closeContextMenu,
        contextMenuState,
        handleKey,
    } from "$lib/stores/globalUi";
    import type { ContextMenuState } from "$lib/types/ui";
    import { keepFocusInside } from "$lib/utils/focus";
    import { blockScrolling } from "$lib/utils/scroll";

    let contextMenu: HTMLElement | undefined = undefined;
    let resizeObserver: ResizeObserver | undefined = undefined;

    let removeFocusTrap: (() => void) | undefined = undefined;
    let escapeUnsubscriber: (() => void) | undefined = undefined;
    let removeScrollTrap: (() => void) | undefined = undefined;

    onMount(() => {
        return closeContextMenu;
    });

    onMount(() => {
        return contextMenuState.subscribe(($contextMenuState) => {
            if (!contextMenu) {
                throw new Error("Expected contextMenu");
            }
            if ($contextMenuState.kind === "visible") {
                if (resizeObserver) {
                    throw new Error("There already was a resizeObserver");
                }
                removeFocusTrap = keepFocusInside(contextMenu);
                addObserver(contextMenu, $contextMenuState);
                escapeUnsubscriber = handleKey("Escape", closeContextMenu);
                removeScrollTrap = blockScrolling();
            } else {
                if (removeFocusTrap) {
                    removeFocusTrap();
                    removeFocusTrap = undefined;
                }
                clearObserver();
                if (escapeUnsubscriber) {
                    escapeUnsubscriber();
                    escapeUnsubscriber = undefined;
                }
                if (removeScrollTrap) {
                    removeScrollTrap();
                }
            }
        });
    });

    onMount(() => {
        return () => {
            // It follows that when a context menu is visible, there is a focus
            // lock. Might be a good chance to do an integrity check here.
            if (removeFocusTrap) {
                removeFocusTrap();
                removeFocusTrap = undefined;
            }
            // One for good measure
            clearObserver();
            // Think about whether this one is necessary
            if (escapeUnsubscriber) {
                escapeUnsubscriber();
                escapeUnsubscriber = undefined;
            }
            if (removeScrollTrap) {
                removeScrollTrap();
            }
        };
    });

    function addObserver(
        contextMenu: HTMLElement,
        $contextMenuState: ContextMenuState & { kind: "visible" },
    ) {
        console.debug($contextMenuState);
        const anchor = $contextMenuState.anchor;
        resizeObserver = new ResizeObserver(() =>
            repositionContextMenu(anchor),
        );
        resizeObserver.observe(contextMenu);
    }

    /*
     * disconnect resizeObserver, if it exists
     */
    function clearObserver() {
        if (resizeObserver === undefined) {
            return;
        }
        resizeObserver.disconnect();
        resizeObserver = undefined;
    }

    function repositionContextMenu(anchor: HTMLElement) {
        if (!contextMenu) {
            throw new Error("Expected contextMenu");
        }
        if (contextMenu.offsetWidth == 0) {
            console.debug("waiting for contextMenu to grow");
            return;
        }
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
            viewPortHeight - (anchorTop + anchor.offsetHeight),
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
    }
</script>

<button
    class="bg-red fixed left-0 top-0 h-full w-full"
    class:hidden={$contextMenuState.kind === "hidden"}
    on:click={closeContextMenu}
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
<!-- This is how we catch the focus leaving the contex menu for a focusable
    element after this. If this is inside an iframe or something, we could
    accidentally leave the iframe... -->
<button class="fixed h-0 w-0" aria-hidden="true" />
