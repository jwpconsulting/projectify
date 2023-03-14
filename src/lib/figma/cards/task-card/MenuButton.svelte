<script lang="ts">
    import { moveTaskAfter, deleteTask } from "$lib/repository/workspace";
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { DotsHorizontal } from "@steeze-ui/heroicons";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection | null;
    let dropDownMenuBtnRef: HTMLElement;

    function openDropDownMenu() {
        if (!workspaceBoardSection) {
            throw new Error("Expected workspaceBoardSection");
        }
        const uuid = workspaceBoardSection.uuid;
        if (!workspaceBoardSection.tasks) {
            throw new Error("Expected workspaceBoardSection.tasks");
        }
        const tasks = workspaceBoardSection.tasks;
        let lastTask = tasks[tasks.length - 1];
        let prevTask = tasks[tasks.indexOf(task) - 1];
        let nextTask = tasks[tasks.indexOf(task) + 1];
        let isFirst = task.uuid == tasks[0].uuid;
        let isLast = task.uuid == lastTask.uuid;
        // TODO show menu
    }
</script>

<button
    class="flex h-5 w-5 flex-row items-center"
    bind:this={dropDownMenuBtnRef}
    on:click|stopPropagation={openDropDownMenu}
    ><Icon
        src={DotsHorizontal}
        theme="outline"
        class="h-5 w-5 text-base-content"
    /></button
>
