<script lang="ts">
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;

    let userPickerBtnRef: HTMLElement;

    $: workspaceUserAssignment = createWorkspaceUserAssignment(task);

    $: assignee = $workspaceUserAssignment;

    async function openUserPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateMember",
            workspaceUserAssignment,
        };
        await openContextMenu(contextMenuType, userPickerBtnRef);
        const workspaceUser = $workspaceUserAssignment;
        await updateTask(
            task,
            task.labels.map((label) => label.uuid),
            workspaceUser
        );
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
