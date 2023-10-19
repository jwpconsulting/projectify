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
            title: $_("help.basics"),
            href: "/help/basics",
        },
        {
            title: $_("help.workspaces"),
            href: "/help/workspaces",
        },
        {
            title: $_("help.boards"),
            href: "/help/boards",
        },
        {
            title: $_("help.sections"),
            href: "/help/sections",
        },
        {
            title: $_("help.tasks"),
            href: "/help/tasks",
        },
        {
            title: $_("help.labels"),
            href: "/help/labels",
        },
        {
            title: $_("help.workspace-users"),
            href: "/help/workspace-users",
        },
        {
            title: $_("help.bulk-select"),
            href: "/help/bulk-select",
        },
        {
            title: $_("help.filters"),
            href: "/help/filters",
        },
        {
            title: $_("help.notifications"),
            href: "/help/notifications",
        },
        {
            title: $_("help.pop-ups"),
            href: "/help/pop-ups",
        },
        {
            title: $_("help.billing"),
            href: "/help/billing",
        },
    ];
</script>

<div class="mx-4 flex w-96 flex-col px-4 sm:w-72">
    {#each helpItems as helpItem}
        <ContextMenuButton
            kind={{ kind: "a", href: helpItem.href }}
            label={helpItem.title}
            state="normal"
            icon={null}
        />
    {/each}
</div>
