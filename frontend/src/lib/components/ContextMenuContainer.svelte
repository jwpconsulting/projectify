<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 Saki Adachi -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { onMount } from "svelte";

    import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
    import { closeContextMenu, contextMenuState } from "$lib/stores/globalUi";
    import { keepFocusInside } from "$lib/utils/focus";
    import { onResize } from "$lib/utils/resize";
    import { onScroll } from "$lib/utils/scroll";
    import { handleKey } from "$lib/utils/keyboard";

    let contextMenu: HTMLElement;

    interface Unsubscribers {
        removeResizeObserver: () => void;
        removeMutationObserver: () => void;
        removeFocusTrap: () => void;
        removeEscapeSubscriber: () => void;
        removeScrollTrap: () => void;
        removeResizeListener: () => void;
    }
    let unsubscribers: Unsubscribers | undefined = undefined;

    onMount(() => {
        return closeContextMenu;
    });

    onMount(() => {
        return contextMenuState.subscribe(($contextMenuState) => {
            if ($contextMenuState.kind === "visible") {
                if (unsubscribers) {
                    throw new Error("Unsubscribers were already set");
                }
                const { anchor } = $contextMenuState;

                const callback = () => repositionContextMenu(anchor);

                unsubscribers = {
                    removeFocusTrap: keepFocusInside(contextMenu),
                    removeResizeObserver: addResizeObserver(
                        contextMenu,
                        callback,
                    ),
                    removeMutationObserver: addMutationObserver(
                        anchor,
                        callback,
                    ),
                    removeEscapeSubscriber: handleKey(
                        "Escape",
                        closeContextMenu,
                    ),
                    removeScrollTrap: onScroll(callback),
                    removeResizeListener: onResize(callback),
                };
            } else {
                clearTraps();
            }
        });
    });

    onMount(() => {
        return clearTraps;
    });

    function clearTraps() {
        if (!unsubscribers) {
            return;
        }
        console.debug("Clearing traps");
        unsubscribers.removeFocusTrap();
        unsubscribers.removeResizeObserver();
        unsubscribers.removeMutationObserver();
        unsubscribers.removeEscapeSubscriber();
        unsubscribers.removeScrollTrap();
        unsubscribers.removeResizeListener();
        unsubscribers = undefined;
    }

    /**
     * Observe changes made to context menu size
     */
    function addResizeObserver(
        contextMenu: HTMLElement,
        callback: () => void,
    ): () => void {
        const resizeObserver = new ResizeObserver(callback);
        resizeObserver.observe(contextMenu);
        return () => resizeObserver.disconnect();
    }

    /**
     * Observe changes made to context menu anchor
     */
    function addMutationObserver(
        anchor: HTMLElement,
        callback: () => void,
    ): () => void {
        const mutationObserver = new MutationObserver(callback);
        const mutationObserverConfig: MutationObserverInit = {
            childList: true,
        };
        mutationObserver.observe(anchor, mutationObserverConfig);
        return () => mutationObserver.disconnect();
    }

    function repositionContextMenu(anchor: HTMLElement) {
        if (anchor.offsetParent === null) {
            console.debug(
                "Context menu anchor not rendered, closing context menu.",
            );
            closeContextMenu();
            return;
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
            bottom: anchorBottom,
        } = anchor.getBoundingClientRect();
        console.debug({ anchor, anchorLeft, anchorTop });

        // Width of viewPort excluding scrollbars
        const { clientWidth: viewPortWidth } = document.body;
        // Height of viewport
        const { innerHeight: viewPortHeight } = window;
        console.debug({ viewPortWidth, viewPortHeight });

        if (anchorTop > viewPortHeight || anchorBottom < 0) {
            console.debug("anchor left viewport");
            closeContextMenu();
            return;
        }
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
            viewPortHeight - anchorBottom,
        );
        // Calculate how many pixels high the context menu is
        // If the context menu takes up more pixels, then reposition the
        // context menu to be above the anchor
        const contextMenuTop =
            contextMenuHeight > anchorBottomToViewPortBottom
                ? // Subtract the overlap from y
                  anchorTop - contextMenuHeight
                : // Else position it under the anchor;
                  anchorBottom;

        console.debug({
            anchorBottomToViewPortBottom,
            contextMenuLeft,
            contextMenuTop,
        });
        contextMenu.style.left = `${contextMenuLeft.toString()}px`;
        contextMenu.style.top = `${contextMenuTop.toString()}px`;
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
