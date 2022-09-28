<script lang="ts">
    export let label: string;
    export let href: string;
    export let active: boolean;
    export let grow: boolean = false;
</script>

<a
    {href}
    class="border-b-2 p-2.5 text-sm font-bold uppercase hover:text-base-content"
    class:border-base-content={active}
    class:border-border={!active}
    class:text-base-content={active}
    class:text-utility={!active}
>
    {label}
</a>
{#if grow}
    <div class="grow border-b-2 border-border" />
{/if}
