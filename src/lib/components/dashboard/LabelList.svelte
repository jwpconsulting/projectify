<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import LabelPill from "$lib/components/dashboard/LabelPill.svelte";
    import Fuse from "fuse.js";
    import type { Label } from "$lib/types/workspace";

    export let labels: Label[];
    export let editable = false;
    export let searchText = "";

    let searchEngine: Fuse<Label> | null = null;
    let filteredLabels: Label[] = [];
    $: {
        searchEngine = new Fuse(labels, {
            keys: ["name"],
        });
        if (searchText.length) {
            filteredLabels = searchEngine
                .search(searchText)
                .map((res: Fuse.FuseResult<Label>) => res.item);
        } else {
            filteredLabels = labels;
        }
    }

    let dispatch = createEventDispatcher();

    export let selectedLabels: Label[] = [];
    let selectedLabelsInx = new Map<string, boolean>();

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
            selectedLabelsInx.set(label.uuid, true);
            selectedLabels.push(label);
            dispatch("addLabel", label);
        } else {
            selectedLabelsInx.delete(label.uuid);
            dispatch("removeLabel", label);
        }

        dispatch("selectionChanged", selectedLabels);
    }

    $: {
        selectedLabels.forEach((label) => {
            selectedLabelsInx.set(label.uuid, true);
        });
    }
</script>

{#each filteredLabels as label}
    <div
        on:click|preventDefault={() => onLabelClick(label)}
        on:keydown|preventDefault={() => onLabelClick(label)}
        class:cursor-pointer={editable}
        class:hover:opacity-60={editable}
        class="cursor-pointer transition-opacity duration-300 ease-out"
    >
        {#if $$slots.item}
            <slot
                name="item"
                {label}
                active={selectedLabelsInx.get(label.uuid)}
            />
        {:else}
            <LabelPill {label} />
        {/if}
    </div>
{/each}
