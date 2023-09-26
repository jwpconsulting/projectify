<script lang="ts">
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";

    import LabelList from "$lib/components/dashboard/LabelList.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { Label, Task } from "$lib/types/workspace";

    export let task: Task;
    let labelPickerBtnRef: HTMLElement;

    $: labelAssignment = createLabelAssignment(task);

    async function openLabelPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateLabel",
            labelAssignment,
        };
        // TODO
        // get the result of the picked label here?
        await openContextMenu(contextMenuType, labelPickerBtnRef);
        const labels: Label[] = $labelAssignment;
        // TODO can we make updateTask accept whole labels instead?
        // TODO skip update when no changes detected
        await updateTask(
            task,
            labels.map((label) => label.uuid),
            task.assignee
        );
    }
</script>

{#if task.labels.length}
    <div class="flex flex-row">
        <LabelList labels={$labelAssignment} />
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
