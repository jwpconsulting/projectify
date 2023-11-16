<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    interface HelpItem {
        title: string;
        href: string;
    }
    let helpItems: HelpItem[];
    $: helpItems = [
        {
            title: $_("help.overview"),
            href: "/help",
        },
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

<nav class="flex flex-col gap-4">
    <h2 class="text-3xl font-bold">
        {$_("help.help-sections")}
    </h2>
    <ul class="flex min-w-max list-inside list-disc flex-col gap-2">
        {#each helpItems as helpItem}
            <li>
                <Anchor href={helpItem.href} label={helpItem.title} />
            </li>
        {/each}
    </ul>
</nav>
