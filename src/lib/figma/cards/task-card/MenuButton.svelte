<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        TaskWithWorkspaceBoardSection,
        WorkspaceBoardDetail,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;
    export let workspaceBoard: WorkspaceBoardDetail;
    // TODO section already contained in task
    export let workspaceBoardSection: WorkspaceBoardSection | undefined;

    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        // TODO task already has workspaceBoardSection
        if (!workspaceBoardSection) {
            throw new Error("Expected workspaceBoardSection");
        }
        const contextMenu: ContextMenuType = {
            kind: "task" as const,
            task,
            location: "dashboard" as const,
            workspaceBoardSection,
            workspaceBoard,
        };
        await openContextMenu(contextMenu, dropDownMenuBtnRef);
        // TODO
        // let lastTask = tasks[tasks.length - 1];
        // let prevTask = tasks[tasks.indexOf(task) - 1];
        // let nextTask = tasks[tasks.indexOf(task) + 1];
        // let isFirst = task.uuid == tasks[0].uuid;
        // let isLast = task.uuid == lastTask.uuid;
        // TODO show menu
    }

    const action = { kind: "button" as const, action: openDropDownMenu };
</script>

<div bind:this={dropDownMenuBtnRef}>
    <CircleIcon icon="ellipsis" size="medium" {action} />
</div>
