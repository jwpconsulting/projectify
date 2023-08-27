<script lang="ts">
    import type { Readable } from "svelte/store";

    import type { Overlay } from "$lib/types/ui";

    export let store: Readable<Overlay<unknown, unknown>>;
</script>

{#if $store.kind === "visible"}
    <div
        class="fixed left-0 top-0 flex h-screen w-screen items-center justify-center bg-black/50"
    >
        <slot target={$store.target} />
    </div>
{/if}
