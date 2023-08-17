<script lang="ts">
    import IconPlus from "$lib/components/icons/icon-plus.svelte";
    import IconSearch from "$lib/components/icons/icon-search.svelte";
</script>

<div
    class="flex h-fit w-fit flex-row items-center gap-2 rounded-lg border border-border p-2 hover:bg-task-hover focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:bg-task-pressed"
>
    <IconSearch />
    <div class="flex flex-row items-center gap-1">
        <div class="rounded-lg border border-border px-2 py-1 text-xs">⌘</div>
        <IconPlus />
        <div class="rounded-lg border border-border px-2 py-1 text-xs">K</div>
    </div>
</div>
