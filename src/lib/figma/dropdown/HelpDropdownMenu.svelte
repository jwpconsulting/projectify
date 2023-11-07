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
            title: $_("help.workspace-boards.title"),
            href: "/help/workspace-boards",
        },
        {
            title: $_("help.workspace-board-sections.title"),
            href: "/help/workspace-board-sections",
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
            title: $_("help.filters.title"),
            href: "/help/filters",
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
