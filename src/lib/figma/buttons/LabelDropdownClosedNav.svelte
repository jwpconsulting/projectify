<script lang="ts">
    // Refactor these
    // TODO Justus 2023-05-03
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard/ui";
    import type { LabelSearchStore } from "$lib/types/stores";

    export let labelSearchModule: LabelSearchStore;

    const { select, selected, searchResults } = labelSearchModule;
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="label"
        action={{ kind: "button", action: toggleLabelDropdownClosedNavOpen }}
        active={$selected.kind !== "allLabels"}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectLabelCheckBox
                label={{ kind: "allLabels" }}
                checked={$selected.kind === "allLabels"}
                on:selected={() => select({ kind: "allLabels" })}
            />
            <SelectLabelCheckBox
                label={{ kind: "noLabel" }}
                checked={$selected.kind === "noLabel"}
                on:selected={() => select({ kind: "noLabel" })}
            />
            {#each $searchResults as label}
                <SelectLabelCheckBox
                    label={{ kind: "label", label: label }}
                    checked={$selected.kind === "labels"
                        ? $selected.labelUuids.has(label.uuid)
                        : false}
                    on:selected={() =>
                        select({
                            kind: "label",
                            labelUuid: label.uuid,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
