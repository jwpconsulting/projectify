<script lang="ts">
    // Refactor these
    // TODO Justus 2023-05-03
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        filterByLabel,
        selectedLabels,
        labelFilterSearchResults,
        unfilterByLabel,
    } from "$lib/stores/dashboard/labelFilter";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard/ui";
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
            <SelectLabelCheckBox
                label={{ kind: "allLabels" }}
                checked={$selectedLabels.kind === "allLabels"}
                onCheck={() => filterByLabel({ kind: "allLabels" })}
                onUncheck={() => unfilterByLabel({ kind: "allLabels" })}
            />
            <SelectLabelCheckBox
                label={{ kind: "noLabel" }}
                checked={$selectedLabels.kind === "noLabel"}
                onCheck={() => filterByLabel({ kind: "noLabel" })}
                onUncheck={() => unfilterByLabel({ kind: "noLabel" })}
            />
            {#each $labelFilterSearchResults as label}
                <SelectLabelCheckBox
                    label={{ kind: "label", label: label }}
                    checked={$selectedLabels.kind === "labels"
                        ? $selectedLabels.labelUuids.has(label.uuid)
                        : false}
                    onCheck={() =>
                        filterByLabel({
                            kind: "label",
                            labelUuid: label.uuid,
                        })}
                    onUncheck={() =>
                        unfilterByLabel({
                            kind: "label",
                            labelUuid: label.uuid,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
