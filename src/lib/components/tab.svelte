<script lang="ts">
    import { getContext } from "svelte";
    import type { Writable } from "svelte/store";

    export let id: string;
    let { activeTabId } = getContext("tabs") as {
        activeTabId: Writable<string>;
    };
</script>

{#if $activeTabId == id}
    <slot />
{/if}
