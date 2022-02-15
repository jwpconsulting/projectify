<script lang="ts" context="module">
    export type ToolBarItem = {
        label: string;
        icon: any;
        onClick: (...any) => void;
    };
</script>

<script lang="ts">
    export let items: ToolBarItem[];
</script>

{#each items as it}
    <button
        class="btn btn-ghost btn-xs h-10 px-3 flex justify-center items-center shrink-0"
        on:click|stopPropagation={it.onClick}
    >
        <svelte:component this={it.icon} />
        <span>{it.label}</span>
    </button>
{/each}
