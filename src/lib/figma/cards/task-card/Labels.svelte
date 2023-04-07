<script lang="ts">
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";
    import LabelList from "$lib/components/dashboard/LabelList.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    let labelPickerBtnRef: HTMLElement;

    function openLabelPicker() {
        // TODO
        console.error("TODO", labelPickerBtnRef);
    }
</script>

{#if task.labels.length}
    <LabelList editable={false} labels={task.labels} />
{:else}
    <div class="p-0.5">
        <button
            class="flex flex-row items-center rounded-xl border border-dashed border-primary px-4 py-1 text-xxs font-bold text-primary"
            bind:this={labelPickerBtnRef}
            on:click|stopPropagation={() => openLabelPicker()}
        >
            {$_("add-label")}</button
        >
    </div>
{/if}
