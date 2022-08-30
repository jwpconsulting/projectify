<script lang="ts">
    import DestructiveOverlay from "$lib/figma/DestructiveOverlay.svelte";
    import {
        destructiveOverlayState,
        closeDestructiveOverlay,
        performDestructiveOverlay,
    } from "$lib/stores/global-ui";

    export let fixed: boolean = true;

    function close() {
        closeDestructiveOverlay();
    }

    function perform() {
        performDestructiveOverlay();
    }
</script>

{#if $destructiveOverlayState.kind === "visible"}
    <div
        class:fixed
        class="top-0 left-0 flex h-screen w-screen items-center justify-center bg-black/50"
    >
        <DestructiveOverlay
            target={$destructiveOverlayState.target}
            on:cancel={close}
            on:destroy={perform}
        />
    </div>
{/if}
