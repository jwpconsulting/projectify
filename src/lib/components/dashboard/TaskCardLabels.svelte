<script lang="ts">
    import { _ } from "svelte-i18n";
    import LabelList from "$lib/components/dashboard/LabelList.svelte";
    import LabelPicker from "./LabelPicker.svelte";
    import { getDropDown } from "../globalDropDown.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    let labelPickerBtnRef: HTMLElement;

    function openLabelPicker() {
        let dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.openComponent(LabelPicker, labelPickerBtnRef, {
            task,
            dispatch: async (_name: string, _data: any) => {
                if (!dropDown) {
                    throw new Error("Expected dropDown");
                }
                dropDown.close();
            },
        });
    }
</script>

{#if task.labels.length}
    <LabelList editable={false} labels={task.labels} />
{:else}
    <div class="p-0.5">
        <div
            class="flex flex-row items-center rounded-xl border border-dashed border-primary px-4 py-1"
        >
            <button
                class="text-xxs font-bold text-primary"
                bind:this={labelPickerBtnRef}
                on:click|stopPropagation={() => openLabelPicker()}
                >{$_("add-label")}</button
            >
        </div>
    </div>
{/if}
