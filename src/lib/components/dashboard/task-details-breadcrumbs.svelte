<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;

    type PathLink = {
        label: string;
    };

    let pathLinks: PathLink[];
    if (
        task.workspace_board_section &&
        task.workspace_board_section.workspace_board
    ) {
        pathLinks = [
            {
                label: task.workspace_board_section.workspace_board.title,
            },
            {
                label: task.workspace_board_section.title,
            },
            {
                label: `#${task.number}`,
            },
        ];
    } else {
        pathLinks = [];
    }
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
