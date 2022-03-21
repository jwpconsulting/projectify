<script lang="ts">
    import { setContext } from "svelte";
    import { writable } from "svelte/store";

    export let items = [];
    export let activeTabId = writable(1);

    setContext("tabs", {
        activeTabId,
    });

    let contentHeght = 0;
    const selectTab = (tabId) => {
        activeTabId.set(tabId);
    };

    export let forceHeight = false;
</script>

<ul class="tabs px-6">
    {#each items as item}
        <li
            class:tab-active={$activeTabId === item.id}
            class="tab tab-bordered font-bold uppercase"
        >
            <span on:click={() => selectTab(item.id)}>{item.label}</span>
        </li>
    {/each}
    <div class="h-[2px] grow bg-base-300" />
</ul>
{#each items as item}
    {#if $activeTabId == item.id}
        <main
            style={forceHeight && `height:${contentHeght}px`}
            class="grow flex flex-col relative overflow-y-auto transition-all ease-in-out duration-300"
        >
            <div
                bind:clientHeight={contentHeght}
                class="flex flex-col px-6 py-4 "
            >
                {#if item.component}
                    <svelte:component this={item.component} {...item.props} />
                {:else}
                    <slot />
                {/if}
            </div>
        </main>
    {/if}
{/each}
