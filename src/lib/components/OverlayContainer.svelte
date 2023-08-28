<script lang="ts">
    import type { Readable } from "svelte/store";

    import type { Overlay } from "$lib/types/ui";

    export let store: Readable<Overlay<unknown, unknown>>;

    export let fixed = true;
</script>

{#if $$slots.else}
    <div class="h-full" class:hidden={$store.kind !== "hidden"}>
        <slot name="else" />
    </div>
{/if}
{#if $store.kind === "visible"}
    <div
        class="left-0 flex items-center justify-center bg-black/50"
        class:fixed
        class:top-0={fixed}
        class:h-screen={fixed}
        class:w-screen={fixed}
        class:absolute={!fixed}
        class:-top-0.5={!fixed}
        class:h-full={!fixed}
        class:w-full={!fixed}
    >
        <slot target={$store.target} />
    </div>
{/if}
