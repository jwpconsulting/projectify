<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { DotsHorizontal } from "@steeze-ui/heroicons";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { MoveTaskModule } from "$lib/types/stores";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection | null;
    export let moveTaskModule: MoveTaskModule | undefined;

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
        const contextMenu: ContextMenuType = {
            kind: "task" as const,
            task,
            location: "dashboard" as const,
            moveTaskModule,
        };
        console.log("TODO use", { uuid, tasks });
        openContextMenu(contextMenu, dropDownMenuBtnRef);
        // TODO
        // let lastTask = tasks[tasks.length - 1];
        // let prevTask = tasks[tasks.indexOf(task) - 1];
        // let nextTask = tasks[tasks.indexOf(task) + 1];
        // let isFirst = task.uuid == tasks[0].uuid;
        // let isLast = task.uuid == lastTask.uuid;
        // TODO show menu
    }
</script>

<button
    class="flex h-5 w-5 flex-row items-center"
    bind:this={dropDownMenuBtnRef}
    on:click|preventDefault={openDropDownMenu}
    ><Icon
        src={DotsHorizontal}
        theme="outline"
        class="h-5 w-5 text-base-content"
    /></button
>
