<script lang="ts">
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";
    import LabelList from "$lib/components/dashboard/LabelList.svelte";
    import type { Task } from "$lib/types/workspace";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType, LabelSelection } from "$lib/types/ui";
    import type { LabelSearchModule } from "$lib/types/stores";
    import { readable, writable } from "svelte/store";

    export let task: Task;
    let labelPickerBtnRef: HTMLElement;

    function openLabelPicker() {
        const selected = readable<LabelSelection>({ kind: "noLabel" });
        const labelSearchModule: LabelSearchModule = {
            select: console.log.bind(null, "Label has been selected"),
            deselect: console.log.bind(null, "Label has been deselected"),
            selected,
            search: writable(""),
            searchResults: readable([]),
        };
        const contextMenuType: ContextMenuType = {
            kind: "updateLabel",
            labelSearchModule,
        };
        // TODO
        openContextMenu(contextMenuType, labelPickerBtnRef);
    }
</script>

{#if task.labels.length}
    <LabelList editable={false} labels={task.labels} />
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
