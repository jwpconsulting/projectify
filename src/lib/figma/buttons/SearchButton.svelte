<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";
</script>

<button
    class="flex flex-row items-center gap-2 rounded-lg border border-border p-2 px-4 hover:bg-task-hover focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:bg-task-pressed"
>
    <Icon src={Search} class="h-6" theme="outline" />
    <p class="min-w-fit">
        {$_("dashboard.search-task")}
    </p>
</button>
