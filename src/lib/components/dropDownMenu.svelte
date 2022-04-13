<script lang="ts" context="module">
    export type DropDownMenuItem = {
        id?: any;
        label: string;
        icon: any;
        onClick?: (...any) => void;
        href?: string;
        disabled?: boolean;
        hidden?: boolean;
        tooltip?: string;
    };
</script>

<script lang="ts">
    let focusEl;
    export let items: DropDownMenuItem[];
    export let activeId: any = null;
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
