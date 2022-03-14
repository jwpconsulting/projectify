<script lang="ts">
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import { getColorFromInx } from "$lib/utils/colors";

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
    <a
        style="{`--color:${getColorFromInx(label.color).style}; --opacity:${
            selectedLabels.length == 0 || selectedLabelsInx[label.uuid]
                ? '1.0'
                : '0.2'
        }`};"
        href="/"
        class="label whitespace-nowrap font-bold text-xs px-3 py-1 m-1 rounded-full border"
        on:click|preventDefault={() => selectLabel(label)}
    >
        {label.name}
    </a>
{/each}
