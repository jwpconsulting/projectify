<script lang="ts">
    import { onMount } from "svelte";

    import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
    import {
        closeContextMenu,
        contextMenuState,
        handleKey,
    } from "$lib/stores/globalUi";
    import { keepFocusInside } from "$lib/utils/focus";
    import { onResize } from "$lib/utils/resize";
    import { blockScrolling } from "$lib/utils/scroll";

    let contextMenu: HTMLElement | undefined = undefined;
    let resizeObserver: ResizeObserver | undefined = undefined;

    let removeFocusTrap: (() => void) | undefined = undefined;
    let escapeUnsubscriber: (() => void) | undefined = undefined;
    let removeScrollTrap: (() => void) | undefined = undefined;
    let removeResizeListener: (() => void) | undefined = undefined;

    onMount(() => {
        return closeContextMenu;
    });

    onMount(() => {
        return contextMenuState.subscribe(($contextMenuState) => {
            if ($contextMenuState.kind === "visible") {
                if (!contextMenu) {
                    throw new Error("Expected contextMenu");
                }
                if (resizeObserver) {
                    throw new Error("There already was a resizeObserver");
                }
                removeFocusTrap = keepFocusInside(contextMenu);
                const { anchor } = $contextMenuState;
                addObserver(contextMenu, anchor);
                escapeUnsubscriber = handleKey("Escape", closeContextMenu);
                removeScrollTrap = blockScrolling();
                removeResizeListener = onResize(
                    repositionContextMenu.bind(null, anchor),
                );
            } else {
                clearTraps();
            }
        });
    });

    onMount(() => {
        return clearTraps;
    });

    function clearTraps() {
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
        if (removeResizeListener) {
            removeResizeListener();
        }
    }

    function addObserver(contextMenu: HTMLElement, anchor: HTMLElement) {
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
        // Width, height of context menu
        const {
            offsetWidth: contextMenuWidth,
            offsetHeight: contextMenuHeight,
        } = contextMenu;
        console.debug({ contextMenuWidth, contextMenuHeight });
        if (contextMenuWidth == 0) {
            console.debug("waiting for contextMenu to grow");
            return;
        }
        // Left, top position of anchor
        // Height of anchor
        const {
            left: anchorLeft,
            top: anchorTop,
            height: anchorHeight,
        } = anchor.getBoundingClientRect();
        console.debug({ anchor, anchorLeft, anchorTop, anchorHeight });
        if (anchorHeight === 0) {
            console.debug(
                "Context menu anchor",
                anchor,
                "is very likely hidden",
            );
            closeContextMenu();
            return;
        }
        // Width, height of viewport
        const { innerWidth: viewPortWidth, innerHeight: viewPortHeight } =
            window;
        console.debug({ viewPortWidth, viewPortHeight });
        // Get x of right side of context menu
        const xRightSide = anchorLeft + contextMenuWidth;
        // Calculate how many pixels the right side of contextMenu will go
        // over the width
        const xOverlap = Math.max(0, xRightSide - viewPortWidth);
        console.debug({ xRightSide, xOverlap });
        // Subtract the overlapy from y
        const contextMenuLeft = anchorLeft - xOverlap;
        // Calculate how many pixels from anchor bottom to viewport bottom
        const anchorBottomToViewPortBottom = Math.abs(
            viewPortHeight - (anchorTop + anchorHeight),
        );
        // Calculate how many pixels high the context menu is
        // If the context menu takes up more pixels, then reposition the
        // context menu to be above the anchor
        const contextMenuTop =
            contextMenuHeight > anchorBottomToViewPortBottom
                ? // Subtract the overlap from y
                  anchorTop - contextMenuHeight
                : // Else position it under the anchor;
                  anchorTop + anchorHeight;

        console.debug({
            anchorBottomToViewPortBottom,
            contextMenuLeft,
            contextMenuTop,
        });
        contextMenu.style.left = `${contextMenuLeft}px`;
        contextMenu.style.top = `${contextMenuTop}px`;
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
