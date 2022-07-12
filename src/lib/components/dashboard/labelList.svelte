<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import LabelPill from "./labelPill.svelte";
    import Fuse from "fuse.js";
    import type { Label } from "$lib/types";

    export let labels: Label[];
    export let editable = false;
    export let searchText = "";
    export let size: "sm" | "md" = "md";

    let searchEngine: Fuse<Label> = null;
    let filteredLabels = [];
    $: {
        searchEngine = new Fuse(labels, {
            keys: ["name"],
        });
    }

    $: {
        if (searchText.length) {
            filteredLabels = searchEngine
                .search(searchText)
                .map((res: Fuse.FuseResult<Label>) => res.item);
        } else {
            filteredLabels = labels;
        }
    }

    let dispatch = createEventDispatcher();

    export let selectedLabels = [];
    $: selectedLabelsInx = selectedLabels && {};

    function onLabelClick(label: Label) {
        if (!editable) {
            return;
        }

        let addLabel = true;
        selectedLabels = selectedLabels.filter((l) => {
            if (l.uuid == label.uuid) {
                addLabel = false;
                return false;
            }
            return true;
        });
        if (addLabel) {
            selectedLabelsInx[label.uuid] = true;
            selectedLabels.push(label);
            dispatch("addLabel", label);
        } else {
            selectedLabelsInx[label.uuid] = false;
            dispatch("removeLabel", label);
        }

        dispatch("selectionChanged", selectedLabels);
    }

    $: {
        selectedLabels.forEach((label) => {
            selectedLabelsInx[label.uuid] = true;
        });
    }
</script>

{#each filteredLabels as label}
    <div
        on:click|preventDefault={() => onLabelClick(label)}
        class:cursor-pointer={editable}
        class:hover:opacity-60={editable}
        class="cursor-pointer transition-opacity duration-300 ease-out"
    >
        {#if $$slots.item}
            <slot name="item" {label} active={selectedLabelsInx[label.uuid]} />
        {:else}
            <LabelPill {size} {label} active={selectedLabelsInx[label.uuid]} />
        {/if}
    </div>
{/each}
