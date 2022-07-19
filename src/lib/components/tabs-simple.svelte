<script lang="ts">
    import type { TabItem } from "$lib/components/types";

    export let items: TabItem[] = [];

    export let activeTabId: string | null = null;
</script>

<ul class="tabs px-4">
    {#each items as item}
        {#if item.hidden !== true}
            <li
                class:tab-active={activeTabId === item.id}
                class="tab tab-bordered font-bold uppercase"
            >
                <a href={item.url}>{item.label}</a>
            </li>
        {/if}
    {/each}
    <div class="h-[2px] grow bg-base-300" />
</ul>
