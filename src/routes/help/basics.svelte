<script lang="ts">
    import { _ } from "svelte-i18n";
    $: sections = [
        {
            title: $_("help-basics.workspace"),
            content: $_("help-basics.workspace-text"),
            id: "workspace",
        },
        {
            title: $_("help-basics.board"),
            content: $_("help-basics.board-text"),
            id: "board",
        },
        {
            title: $_("help-basics.section"),
            content: $_("help-basics.section-text"),
            id: "section",
        },
        {
            title: $_("help-basics.task"),
            content: $_("help-basics.task-text"),
            id: "task",
        },
        {
            title: $_("help-basics.side-menu"),
            content: $_("help-basics.side-menu-text"),
            id: "side-menu",
        },
    ];
</script>

<div class="page bg base-200 space-y-4 p-8 sm:hidden">
    <p class="text-xl font-bold">
        {$_("help.skip")}
    </p>
    <ul class="space-y-1 text-primary">
        {#each sections as section}
            <li>
                <a href={`#${section.id}`}>
                    {section.title}
                </a>
            </li>
        {/each}
    </ul>
</div>

<div class="m-8 space-y-16">
    {#each sections as section}
        <section id="workspace" class="space-y-4">
            <h3 class="text-3xl font-bold">
                {$_("help-basics.workspace")}
            </h3>
            <p>
                {section.content}
            </p>
        </section>
    {/each}
</div>
