<script lang="ts">
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";

    interface HelpItem {
        title: string;
        href: string;
    }
    let helpItems: HelpItem[];
    $: helpItems = [
        {
            title: $_("help.basics.title"),
            href: "/help/basics",
        },
        {
            title: $_("help.workspaces.title"),
            href: "/help/workspaces",
        },
        {
            title: $_("help.boards.title"),
            href: "/help/boards",
        },
        {
            title: $_("help.sections.title"),
            href: "/help/sections",
        },
        {
            title: $_("help.tasks.title"),
            href: "/help/tasks",
        },
        {
            title: $_("help.labels.title"),
            href: "/help/labels",
        },
        {
            title: $_("help.workspace-users.title"),
            href: "/help/workspace-users",
        },
        {
            title: $_("help.bulk-select.title"),
            href: "/help/bulk-select",
        },
        {
            title: $_("help.filters.title"),
            href: "/help/filters",
        },
        {
            title: $_("help.notifications.title"),
            href: "/help/notifications",
        },
        {
            title: $_("help.pop-ups.title"),
            href: "/help/pop-ups",
        },
        {
            title: $_("help.billing.title"),
            href: "/help/billing",
        },
    ];
</script>

<div class="flex flex-col">
    {#each helpItems as helpItem}
        <ContextMenuButton
            kind={{ kind: "a", href: helpItem.href }}
            label={helpItem.title}
            state="normal"
            icon={null}
        />
    {/each}
</div>
