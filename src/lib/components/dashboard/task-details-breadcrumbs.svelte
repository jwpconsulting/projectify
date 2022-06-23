<script lang="ts">
    import { _ } from "svelte-i18n";

    export let task;

    let pathLinks = [
        {
            label: task.workspaceBoardSection.workspaceBoard.title,
        },
        {
            label: task.workspaceBoardSection.title,
        },
        {
            label: `#${task.number}`,
        },
    ];
</script>

<div class="flex max-w-full items-center gap-2 overflow-hidden">
    <div class="breadcrumbs max-w-full text-sm">
        <ul>
            {#each pathLinks as pl}
                <li>
                    <span>{pl.label}</span>
                </li>
            {/each}
        </ul>
    </div>
</div>
