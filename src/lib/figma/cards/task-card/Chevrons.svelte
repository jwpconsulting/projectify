<script lang="ts">
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import { moveTaskAfter } from "$lib/repository/workspace";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection | null = null;
    export let isFirst = false;
    export let isLast = false;

    function moveUp() {
        if (!workspaceBoardSection) {
            throw new Error("Expected workspaceBoardSection");
        }
        if (!workspaceBoardSection.tasks) {
            throw new Error("Expected workspaceBoardSection.tasks");
        }
        let prevTask =
            workspaceBoardSection.tasks[
                workspaceBoardSection.tasks.indexOf(task) - 1
            ];
        moveTaskAfter(task.uuid, workspaceBoardSection.uuid, prevTask?.uuid);
    }

    function moveDown() {
        if (!workspaceBoardSection) {
            throw new Error("Expected workspaceBoardSection");
        }
        if (!workspaceBoardSection.tasks) {
            throw new Error("Expected workspaceBoardSection.tasks");
        }
        let nextTask =
            workspaceBoardSection.tasks[
                workspaceBoardSection.tasks.indexOf(task) + 1
            ];
        moveTaskAfter(task.uuid, workspaceBoardSection.uuid, nextTask?.uuid);
    }
</script>

<div class="flex flex-row items-center gap-1">
    <CircleIcon
        size="medium"
        icon="up"
        disabled={isFirst}
        action={{ kind: "button", action: moveUp }}
    />
    <CircleIcon
        size="medium"
        icon="down"
        disabled={isLast}
        action={{ kind: "button", action: moveDown }}
    />
</div>
