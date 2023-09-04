<script lang="ts">
    import { Plus, Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
</script>

<div
    class="flex h-fit w-fit flex-row items-center gap-2 rounded-lg border border-border p-2 hover:bg-task-hover focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:bg-task-pressed"
>
    <Icon src={Search} class="h-6" theme="outline" />
    <div class="flex flex-row items-center gap-1">
        <div class="rounded-lg border border-border px-2 py-1 text-xs">⌘</div>
        <Icon src={Plus} class="shrink-0 h-6 w-6" theme="outline" />
        <div class="rounded-lg border border-border px-2 py-1 text-xs">K</div>
    </div>
</div>
