<script lang="ts">
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";

    import LabelPill from "$lib/components/dashboard/LabelPill.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        Label,
        TaskWithWorkspaceBoardSection,
    } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;
    $: labelAssignment = createLabelAssignment(task);
    $: labels = $labelAssignment ?? task.labels;

    async function openLabelPicker(event: MouseEvent) {
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        const anchor = event.target;
        if (!(anchor instanceof HTMLElement)) {
            throw new Error("Expected HTMLElement");
        }
        const contextMenuType: ContextMenuType = {
            kind: "updateLabel",
            labelAssignment,
        };
        await openContextMenu(contextMenuType, anchor);
        const labels: Label[] = $labelAssignment;
        // TODO can we make updateTask accept whole labels instead?
        // TODO skip update when no changes detected
        await updateTask(task, labels, task.assignee, task.sub_tasks, {
            fetch,
        });
        // TODO There is a brief flash after updateTask finishes, the task is
        // reloaded and labelAssignment is recreated
    }
</script>

{#if labels.length}
    <div class="flex flex-row">
        {#each labels as label}
            <button on:click|preventDefault={openLabelPicker}>
                <LabelPill {label} />
            </button>
        {/each}
    </div>
{:else}
    <div class="p-0.5">
        <button
            class="flex flex-row items-center rounded-xl border border-dashed border-primary px-4 py-1 text-sm font-bold text-primary"
            on:click|preventDefault={openLabelPicker}
        >
            {$_("dashboard.task-card.add-label")}</button
        >
    </div>
{/if}
