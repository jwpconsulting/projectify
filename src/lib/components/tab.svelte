<script lang="ts">
    import { getContext } from "svelte";

    export let id: string;
    let { activeTabId } = getContext("tabs");
</script>

{#if $activeTabId == id}
    <slot />
{/if}
