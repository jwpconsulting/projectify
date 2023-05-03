<script lang="ts">
    import type { Readable } from "svelte/store";
    import type { Overlay, OverlayComponent } from "$lib/types/ui";

    export let overlay: OverlayComponent;
    export let store: Readable<Overlay<unknown, unknown>>;
    export let close: () => void;
    export let perform: (() => void) | null;
</script>

{#if $store.kind === "visible"}
    <div
        class="fixed left-0 top-0 flex h-screen w-screen items-center justify-center bg-black/50"
    >
        <svelte:component
            this={overlay}
            target={$store.target}
            on:cancel={close}
            on:destroy={perform}
        />
    </div>
{/if}
