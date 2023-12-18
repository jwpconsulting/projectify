<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        filterByLabel,
        unfilterByLabel,
        labelSearch,
        labelFilterSearchResults,
        selectedLabels,
    } from "$lib/stores/dashboard/labelFilter";
    import type { LabelAssignment } from "$lib/types/stores";

    type FilterLabelMenuMode =
        | { kind: "filter" }
        | {
              kind: "assign";
              labelAssignment: LabelAssignment;
          };

    export let mode: FilterLabelMenuMode;
    // Here we need to distinguish between a label menu used to
    // filter tasks by labels
    // or assign a label to a task
    export let canEdit = true;

    $: selected =
        mode.kind === "filter"
            ? selectedLabels
            : mode.labelAssignment.selected;
    $: onCheck =
        mode.kind === "filter" ? filterByLabel : mode.labelAssignment.select;
    $: onUncheck =
        mode.kind === "filter"
            ? unfilterByLabel
            : mode.labelAssignment.deselect;

    $: hasSearchInput = $labelSearch !== "" && $labelSearch !== undefined;
</script>

<div class="flex flex-col px-4 pb-4 pt-2">
    <label for="label-name" class="p-2 text-sm font-bold">
        {$_("filter-label-menu.filter-labels")}
    </label>
    <InputField
        bind:value={$labelSearch}
        label={undefined}
        style={{ inputType: "text" }}
        name="label-name"
        placeholder={$_("filter-label-menu.label-name")}
    >
        <Icon slot="left" src={Search} class="w-4" theme="outline" />
    </InputField>
</div>
<div class="flex flex-col">
    {#if mode.kind == "filter" && hasSearchInput}
        <FilterLabel
            label={{ kind: "allLabels" }}
            checked={$selected.kind === "allLabels"}
            onCheck={() => filterByLabel({ kind: "allLabels" })}
            onUncheck={() => unfilterByLabel({ kind: "allLabels" })}
        />
    {/if}
    <FilterLabel
        label={{ kind: "noLabel" }}
        checked={$selected.kind === "noLabel"}
        onCheck={() => onCheck({ kind: "noLabel" })}
        onUncheck={() => onUncheck({ kind: "noLabel" })}
    />
    {#each $labelFilterSearchResults as label (label.uuid)}
        <FilterLabel
            label={{ kind: "label", label }}
            checked={$selected.kind === "labels"
                ? $selected.labelUuids.has(label.uuid)
                : false}
            {canEdit}
            onCheck={() => onCheck({ kind: "label", labelUuid: label.uuid })}
            onUncheck={() =>
                onUncheck({ kind: "label", labelUuid: label.uuid })}
        />
    {/each}
</div>
