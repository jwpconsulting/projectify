<script lang="ts">
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";

    import LabelList from "$lib/components/dashboard/LabelList.svelte";
    import { assignLabelToTask } from "$lib/repository/workspace";
    import { createLabelSearchStore } from "$lib/stores/dashboard/labelAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { LabelAssignment } from "$lib/types/stores";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    let labelPickerBtnRef: HTMLElement;

    function openLabelPicker() {
        const labelAssignment: LabelAssignment = createLabelSearchStore(
            task,
            (labelUuid: string, selected: boolean) => {
                assignLabelToTask(task, labelUuid, selected);
            }
        );
        const contextMenuType: ContextMenuType = {
            kind: "updateLabel",
            labelAssignment,
        };
        // TODO
        openContextMenu(contextMenuType, labelPickerBtnRef);
    }
</script>

{#if task.labels.length}
    <div class="flex flex-row">
        <LabelList editable={false} labels={task.labels} />
    </div>
{:else}
    <div class="p-0.5">
        <button
            class="flex flex-row items-center rounded-xl border border-dashed border-primary px-4 py-1 text-xxs font-bold text-primary"
            bind:this={labelPickerBtnRef}
            on:click|preventDefault={openLabelPicker}
        >
            {$_("add-label")}</button
        >
    </div>
{/if}
