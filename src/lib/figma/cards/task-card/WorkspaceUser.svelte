<script lang="ts">
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;

    let userPickerBtnRef: HTMLElement;

    function openUserPicker() {
        // TODO
        console.error(
            "TODO do something with task",
            task,
            "and",
            userPickerBtnRef
        );
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
        on:click|stopPropagation={() => openUserPicker()}
    >
        <AvatarVariant content={{ kind: "single", user: null }} size="small" />
    </button>
{/if}
