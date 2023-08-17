<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { moveTaskAfter } from "$lib/repository/workspace";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection | null = null;
    export let isFirst = false;
    export let isLast = false;

    async function moveUp() {
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
        await moveTaskAfter(
            task.uuid,
            workspaceBoardSection.uuid,
            prevTask.uuid
        );
    }

    async function moveDown() {
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
        await moveTaskAfter(
            task.uuid,
            workspaceBoardSection.uuid,
            nextTask.uuid
        );
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
