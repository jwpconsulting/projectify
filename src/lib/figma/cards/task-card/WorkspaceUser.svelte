<script lang="ts">
    import type { Task } from "$lib/types/workspace";
    import WorkspaceUserAvatar from "$lib/components/WorkspaceUserAvatar.svelte";

    export let task: Task;

    let userPickerBtnRef: HTMLElement;

    function openUserPicker() {}
</script>

{#if task.assignee}
    <WorkspaceUserAvatar size={24} workspaceUser={task.assignee} />
{:else}
    <button
        bind:this={userPickerBtnRef}
        on:click|stopPropagation={() => openUserPicker()}
    >
        <WorkspaceUserAvatar workspaceUser={"assign"} size={24} />
    </button>
{/if}
