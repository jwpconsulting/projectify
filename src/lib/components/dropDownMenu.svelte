<script lang="ts" context="module">
    export type DropDownMenuItem = {
        label: string;
        icon: any;
        onClick?: (...any) => void;
        href?: string;
        disabled?: boolean;
        hidden?: boolean;
        tooltip?: string;
    };

    let focusEl;
</script>

<script lang="ts">
    export let items: DropDownMenuItem[];
</script>

<div class="dropdown-end dropdown select-none">
    <slot />
    <ul
        bind:this={focusEl}
        tabindex="0"
        class="dropdown-content menu min-w-[200px] rounded-lg
            bg-base-100 py-2 shadow-xl"
    >
        {#each items as it}
            {#if !it.hidden}
                <li>
                    <a
                        title={it.tooltip}
                        disabled={it.disabled}
                        class="nowrap-ellipsis h-9 space-x-2 px-0 text-xs font-bold"
                        href={it.href}
                        on:click={() => {
                            it.onClick();
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
