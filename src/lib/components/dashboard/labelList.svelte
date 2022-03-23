<script lang="ts">
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import { createEventDispatcher } from "svelte";
    import LabelPill from "./labelPill.svelte";
    import Fuse from "fuse.js";

    export let labels;
    export let editable = false;
    export let searchText = "";
    let searchEngine = null;
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
                .map((res) => res.item);
        } else {
            filteredLabels = labels;
        }
    }

    let dispatch = createEventDispatcher();

    export let selectedLabels = [];
    let selectedLabelsInx = {};
    function onLabelClick(label) {
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
        class="cursor-pointer transition-opacity ease-out duration-300"
    >
        {#if $$slots.item}
            <slot name="item" {label} active={selectedLabelsInx[label.uuid]} />
        {:else}
            <LabelPill
                {label}
                active={selectedLabels.length == 0 ||
                    selectedLabelsInx[label.uuid]}
            />
        {/if}
    </div>
{/each}
