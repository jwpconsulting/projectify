<script lang="ts">
    import {
        currentWorkspace,
        selectedLabels,
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        selectLabel,
    } from "$lib/stores/dashboard";
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import SquovalIcon from "$lib/figma/buttons/SquovalIcon.svelte";
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="label"
        action={{ kind: "button", action: toggleLabelDropdownClosedNavOpen }}
        active={$selectedLabels.kind !== "allLabels"}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            {#if $currentWorkspace && $currentWorkspace.labels}
                <SelectLabelCheckBox
                    label={{ kind: "allLabels" }}
                    checked={$selectedLabels.kind === "allLabels"}
                    on:selected={() => selectLabel({ kind: "allLabels" })}
                />
                <SelectLabelCheckBox
                    label={{ kind: "noLabel" }}
                    checked={$selectedLabels.kind === "noLabel"}
                    on:selected={() => selectLabel({ kind: "noLabel" })}
                />
                {#each $currentWorkspace.labels as label}
                    <SelectLabelCheckBox
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
