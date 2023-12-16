<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        TaskWithWorkspaceBoardSection,
        WorkspaceBoardDetail,
        WorkspaceBoardSectionWithTasks,
    } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;
    // this is only ever needed for the dashboard, not when a task is part
    // of search results... time for another ADT?
    export let workspaceBoard: WorkspaceBoardDetail;
    export let workspaceBoardSection:
        | WorkspaceBoardSectionWithTasks
        | undefined = undefined;

    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        const contextMenu: ContextMenuType =
            workspaceBoardSection === undefined
                ? {
                      kind: "task",
                      task,
                      location: "task",
                      workspaceBoardSection: task.workspace_board_section,
                  }
                : {
                      kind: "task" as const,
                      task,
                      location: "dashboard" as const,
                      workspaceBoardSection,
                      workspaceBoard,
                  };
        await openContextMenu(contextMenu, dropDownMenuBtnRef);
    }

    const action = { kind: "button" as const, action: openDropDownMenu };
</script>

<div bind:this={dropDownMenuBtnRef}>
    <CircleIcon icon="ellipsis" size="medium" {action} />
</div>
