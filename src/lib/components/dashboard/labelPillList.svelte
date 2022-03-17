<script lang="ts">
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import { getColorFromInx } from "$lib/utils/colors";
    import LabelPill from "./labelPill.svelte";

    export let selectedLabels = [];
    let selectedLabelsInx = {};
    function selectLabel(label) {
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
        } else {
            selectedLabelsInx[label.uuid] = false;
        }
    }
</script>

{#each $currentWorkspaceLabels as label}
    <div
        on:click|preventDefault={() => selectLabel(label)}
        class="cursor-pointer"
    >
        <LabelPill
            {label}
            active={selectedLabels.length == 0 ||
                selectedLabelsInx[label.uuid]}
        />
    </div>
{/each}
