<script lang="ts">
    import ContextMenu from "$lib/figma/overlays/ContextMenu.svelte";
    import { contextMenuState, closeContextMenu } from "$lib/stores/global-ui";

    let contextMenu: HTMLElement;
    let resizeObserver: ResizeObserver | null;
    let repositioned = false;
    contextMenuState.subscribe(($contextMenuState) => {
        if ($contextMenuState.kind === "visible") {
            if (!contextMenu) {
                throw new Error("Could not find contextMenu");
            }
            const anchor = $contextMenuState.anchor;
            repositioned = false;
            resizeObserver = new ResizeObserver(() =>
                repositionContextMenu(anchor)
            );
            resizeObserver.observe(contextMenu);
        } else {
            resizeObserver = null;
        }
    });

    function repositionContextMenu(anchor: HTMLElement) {
        if (repositioned) {
            console.debug("already repositioned");
            return;
        }
        if (contextMenu.offsetWidth == 0) {
            console.log("waiting for contextMenu to grow");
            return;
        }
        console.log("repositioning");
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
        console.log("offsetWidth", contextMenu.offsetWidth);
        console.log({ viewPortWidth, anchorLeft, xRightSide, xOverlap });
        if (xOverlap > 0) {
            console.log("xOverlap", xOverlap);
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

<div
    class="fixed left-0 top-0 h-screen w-screen bg-transparent"
    class:invisible={$contextMenuState.kind === "hidden"}
    on:click={closeContextMenu}
    on:keydown={closeContextMenu}
/>
<div
    class="fixed"
    bind:this={contextMenu}
    on:click={closeContextMenu}
    on:keydown={closeContextMenu}
>
    {#if $contextMenuState.kind === "visible"}
        <ContextMenu target={$contextMenuState.target} />
    {/if}
</div>
