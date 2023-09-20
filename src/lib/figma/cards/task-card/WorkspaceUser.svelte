<script lang="ts">
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { createWorkspaceUserSearchStore } from "$lib/stores/dashboard/workspaceUserAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;

    let userPickerBtnRef: HTMLElement;

    function openUserPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateMember",
            workspaceUserAssignment: createWorkspaceUserSearchStore(task),
        };
        openContextMenu(contextMenuType, userPickerBtnRef);
    }
</script>

{#if task.assignee}
    <AvatarVariant
        content={{ kind: "single", user: task.assignee.user }}
        size="small"
    />
{:else}
    <button
        bind:this={userPickerBtnRef}
        on:click|preventDefault={() => openUserPicker()}
    >
        <AvatarVariant content={{ kind: "single", user: null }} size="small" />
    </button>
{/if}
