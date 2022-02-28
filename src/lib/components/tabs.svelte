<script lang="ts">
    export let items = [];
    export let activeTabId = 1;
    let contentHeght = 0;
    const handleClick = (tabId) => () => (activeTabId = tabId);

    import { fade } from "svelte/transition";
</script>

<ul class="tabs">
    {#each items as item}
        <li
            class:tab-active={activeTabId === item.id}
            class="tab tab-bordered font-bold uppercase"
        >
            <span on:click={handleClick(item.id)}>{item.label}</span>
        </li>
    {/each}
    <div class="h-[2px] grow bg-base-300" />
</ul>
{#each items as item}
    {#if activeTabId == item.id}
        <main
            style="height:{contentHeght}px"
            class="flex flex-col relative overflow-hidden transition-all ease-in-out duration-300"
        >
            <div bind:clientHeight={contentHeght} class="flex flex-col pt-4">
                <svelte:component this={item.component} {...item.props} />
            </div>
        </main>
    {/if}
{/each}
