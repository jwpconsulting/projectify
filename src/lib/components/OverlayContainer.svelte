<script lang="ts">
    import type { Readable } from "svelte/store";
    import type { Overlay, OverlayComponent } from "$lib/types/ui";

    export let overlay: OverlayComponent;
    export let store: Readable<Overlay<any, any>>;
    export let close: () => void;
    export let perform: () => void;
</script>

{#if $store.kind === "visible"}
    <div
        class="fixed top-0 left-0 flex h-screen w-screen items-center justify-center bg-black/50"
    >
        <svelte:component
            this={overlay}
            target={$store.target}
            on:cancel={close}
            on:destroy={perform}
        />
    </div>
{/if}
