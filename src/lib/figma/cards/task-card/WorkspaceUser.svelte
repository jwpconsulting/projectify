<script lang="ts">
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { TaskWithWorkspaceBoardSection } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;

    let userPickerBtnRef: HTMLElement;

    $: workspaceUserAssignment = createWorkspaceUserAssignment(task);

    $: assignee = $workspaceUserAssignment;

    async function openUserPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateWorkspaceUser",
            workspaceUserAssignment,
        };
        await openContextMenu(contextMenuType, userPickerBtnRef);
        const workspaceUser = $workspaceUserAssignment;
        // XXX need to investigate what happens when sub tasks change while
        // the user picker is open. Possibly, a sub task can be deleted if
        // it is added
        await updateTask(task, task.labels, workspaceUser, task.sub_tasks);
    }
</script>

{#if assignee}
    <AvatarVariant
        content={{ kind: "single", user: assignee.user }}
        size="small"
    />
{:else}
    <button
        bind:this={userPickerBtnRef}
        on:click|preventDefault={openUserPicker}
    >
        <AvatarVariant content={{ kind: "single", user: null }} size="small" />
    </button>
{/if}
