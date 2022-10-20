<script lang="ts">
    import {
        currentWorkspace,
        selectedLabels,
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        selectLabel,
    } from "$lib/stores/dashboard";
    import SelectLabelFocus from "$lib/figma/select-controls/SelectLabelFocus.svelte";
    import Squoval from "$lib/figma/buttons/Squoval.svelte";
</script>

<div class="flex flex-col items-center gap-6">
    <Squoval
        state="active"
        icon="label"
        on:click={toggleLabelDropdownClosedNavOpen}
        active={$selectedLabels.kind !== "allLabels"}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            {#if $currentWorkspace && $currentWorkspace.labels}
                <SelectLabelFocus
                    label={{ kind: "allLabels" }}
                    checked={$selectedLabels.kind === "allLabels"}
                    on:selected={() => selectLabel({ kind: "allLabels" })}
                />
                <SelectLabelFocus
                    label={{ kind: "noLabel" }}
                    checked={$selectedLabels.kind === "noLabel"}
                    on:selected={() => selectLabel({ kind: "noLabel" })}
                />
                {#each $currentWorkspace.labels as label}
                    <SelectLabelFocus
                        label={{ kind: "label", label: label }}
                        checked={$selectedLabels.kind === "labels"
                            ? $selectedLabels.labelUuids.has(label.uuid)
                            : false}
                        on:selected={() =>
                            selectLabel({
                                kind: "label",
                                labelUuid: label.uuid,
                            })}
                    />
                {/each}
            {/if}
        </div>
    {/if}
</div>
