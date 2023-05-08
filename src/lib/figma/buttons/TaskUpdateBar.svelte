<script lang="ts">
    import { _ } from "svelte-i18n";
    import TabElement from "$lib/figma/buttons/TabElement.svelte";
    import type {
        TaskUpdateBarKind,
        TaskUpdateBarState,
    } from "$lib/figma/types";
    import { getTaskUrl, getTaskUpdatesUrl } from "$lib/urls";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    export let kind: TaskUpdateBarKind;
    export let state: TaskUpdateBarState;

    $: taskUrl = getTaskUrl(task.uuid);
    $: taskUpdatesUrl = getTaskUpdatesUrl(task.uuid);
</script>

{#if kind === "desktop"}
    <div class="flex flex-row">
        {#if state === "task"}
            <TabElement href={taskUrl} label={$_("task")} active />
        {:else}
            <TabElement href={taskUpdatesUrl} label={$_("updates")} active />
        {/if}
        <div class="grow border-b-2 border-base-content" />
    </div>
{:else}
    <div class="flex flex-row">
        <TabElement
            href={taskUrl}
            label={$_("task")}
            active={state === "task"}
        />
        <TabElement
            href={taskUpdatesUrl}
            label={$_("updates")}
            active={state === "updates"}
        />
        <div class="grow border-b-2 border-border" />
    </div>
{/if}
