<script lang="ts">
    import { Plus } from "@steeze-ui/heroicons";
    import type { Readable } from "svelte/store";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        filterByLabel,
        unfilterByLabel,
        labelSearch,
        labelFilterSearchResults,
        selectedLabels,
    } from "$lib/stores/dashboard/labelFilter";
    import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";

    type FilterLabelMenuMode =
        | { kind: "filter" }
        | {
              kind: "assign";
              selected: Readable<LabelSelection>;
              assign: (labelSelectionInput: LabelSelectionInput) => void;
              unassign: (labelSelectionInput: LabelSelectionInput) => void;
          };

    // TODO make this non-optional
    export let mode: FilterLabelMenuMode = { kind: "filter" as const };
    // Here we need to distinguish between a label menu used to
    // filter tasks by labels
    // or assign a label to a task
    export let canEdit = true;
    // If it is null, we don't show the create new label button
    export let startCreateLabel: (() => void) | null = null;

    $: selected = mode.kind === "filter" ? selectedLabels : mode.selected;
</script>

<div class="flex flex-col px-4 pb-4 pt-2">
    <div class="p-2 text-xs font-bold first-letter:capitalize">
        {$_("filter-label-menu.filter-labels")}
    </div>
    <InputField
        bind:value={$labelSearch}
        style={{ kind: "search" }}
        name="label-name"
        placeholder={$_("filter-label-menu.label-name")}
    />
</div>
<div class="flex flex-col">
    {#if $labelSearch === "" && mode.kind == "filter"}
        <FilterLabel
            label={{ kind: "allLabels" }}
            checked={$selected.kind === "allLabels"}
            onCheck={filterByLabel}
            onUncheck={unfilterByLabel}
        />
        <FilterLabel
            label={{ kind: "noLabel" }}
            checked={$selected.kind === "noLabel"}
            onCheck={filterByLabel}
            onUncheck={unfilterByLabel}
        />
    {/if}
    {#each $labelFilterSearchResults as label (label.uuid)}
        <FilterLabel
            label={{ kind: "label", label }}
            checked={$selected.kind === "labels"
                ? $selected.labelUuids.has(label.uuid)
                : false}
            {canEdit}
            onCheck={filterByLabel}
            onUncheck={unfilterByLabel}
        />
    {/each}
    {#if startCreateLabel}
        <!-- Some left padding issues here, not aligned with FilterLabel TODO -->
        <ContextMenuButton
            label={$_("filter-label-menu.create-new-label")}
            icon={Plus}
            state="normal"
            color="primary"
            kind={{ kind: "button", action: startCreateLabel }}
        />
    {/if}
</div>
