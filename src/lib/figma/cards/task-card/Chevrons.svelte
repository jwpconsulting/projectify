<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import { moveTaskAfter } from "$lib/repository/workspace";

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
    <button
        class="p-1.5"
        class:text-base-content={!isFirst}
        class:text-disabled-text={isFirst}
        disabled={isFirst}
        on:click|stopPropagation={() => moveUp()}
    >
        <Icon src={ChevronUp} theme="outline" class="h-5 w-5" />
    </button>
    <button
        class="p-1.5"
        disabled={isLast}
        class:text-base-content={!isLast}
        class:text-disabled-text={isLast}
        on:click|stopPropagation={() => moveDown()}
        ><Icon src={ChevronDown} theme="outline" class="h-5 w-5" /></button
    >
</div>
