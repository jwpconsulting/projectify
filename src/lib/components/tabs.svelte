<script lang="ts">
    import { createEventDispatcher, setContext } from "svelte";
    import { writable } from "svelte/store";
    import type { TabItem } from "$lib/components/types";

    export let items: TabItem[] = [];
    export let activeTabId = writable(items[0]?.id);
    export let dispatcher = createEventDispatcher();

    $: {
        setContext("tabs", {
            activeTabId,
        });
    }

    let contentHeight = 0;
    const selectTab = (tabId: string) => {
        activeTabId.set(tabId);
        dispatcher("tabChanged", { tabId });
    };

    export let forceHeight = false;
    export let autoPadding = true;
</script>

<ul class="tabs px-4">
    {#each items as item}
        {#if item.hidden !== true}
            <li
                class:tab-active={$activeTabId === item.id}
                class="tab tab-bordered font-bold uppercase"
            >
                <span
                    on:click={() => selectTab(item.id)}
                    on:keydown={() => selectTab(item.id)}>{item.label}</span
                >
            </li>
        {/if}
    {/each}
    <div class="h-[2px] grow bg-base-300" />
</ul>
{#each items as item}
    {#if $activeTabId == item.id}
        <main
            style={forceHeight ? `height:${contentHeight}px` : null}
            class="relative flex grow flex-col overflow-y-auto transition-all duration-300 ease-in-out"
        >
            <div
                class:px-4={autoPadding}
                class:py-4={autoPadding}
                bind:clientHeight={contentHeight}
                class="relative flex grow flex-col"
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
