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
</script>

<script lang="ts">
    export let items: DropDownMenuItem[];
</script>

<div class="dropdown dropdown-end">
    <slot />
    <ul
        tabindex="0"
        class="menu dropdown-content bg-base-100 rounded-lg
            min-w-[200px] shadow-xl py-2"
    >
        {#each items as it}
            {#if !it.hidden}
                <li>
                    <a
                        title={it.tooltip}
                        disabled={it.disabled}
                        class="space-x-2 nowrap-ellipsis text-xs font-bold h-9 px-0"
                        href={it.href}
                        on:click={it.onClick}
                    >
                        <svelte:component this={it.icon} />
                        <span>{it.label}</span>
                    </a>
                </li>
            {/if}
        {/each}
    </ul>
</div>
