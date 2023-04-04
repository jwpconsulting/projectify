<script lang="ts" context="module">
    import type { SvelteComponent } from "svelte";

    export type DropDownMenuItem = {
        id?: unknown;
        label: string;
        icon: typeof SvelteComponent;
        onClick?: (...arg0: unknown[]) => void;
        href?: string;
        disabled?: boolean;
        hidden?: boolean;
        tooltip?: string;
    };
</script>

<script lang="ts">
    let focusEl: HTMLElement;
    export let items: DropDownMenuItem[];
    export let activeId: unknown | null = null;
</script>

<div class="dropdown dropdown-end select-none">
    <slot />
    <ul
        bind:this={focusEl}
        tabindex="-1"
        class="dropdown-content menu min-w-[200px] rounded-lg
            border border-base-300 bg-base-100 py-2 shadow-xl"
    >
        {#each items as it}
            {#if !it.hidden}
                <li>
                    <a
                        title={it.tooltip}
                        class:active={activeId === it.id}
                        class="nowrap-ellipsis h-9 space-x-2 px-0 text-xs font-bold"
                        href={it.href}
                        on:click={() => {
                            if (it.onClick) {
                                it.onClick();
                            }

                            focusEl.blur();
                        }}
                    >
                        <svelte:component this={it.icon} />
                        <span>{it.label}</span>
                    </a>
                </li>
            {/if}
        {/each}
    </ul>
</div>
