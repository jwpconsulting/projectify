<script lang="ts">
    import { Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        filterByLabel,
        unfilterByLabel,
    } from "$lib/stores/dashboard/labelFilter";
    import type { LabelAssignment } from "$lib/types/stores";

    export let labelSearchModule: LabelAssignment;
    // Here we need to distinguish between a label menu used to
    // filter tasks by labels
    // or assign a label to a task
    export let canEdit = true;
    // If it is null, we don't show the create new label button
    export let startCreateLabel: (() => void) | null = null;

    const { selected, search, searchResults } = labelSearchModule;
</script>

<div class="flex flex-col px-4 pb-4 pt-2">
    <div class="p-2 text-xs font-bold first-letter:capitalize">
        {$_("filter-label-menu.filter-labels")}
    </div>
    <InputField
        bind:value={$search}
        style={{ kind: "search" }}
        name="label-name"
        placeholder={$_("filter-label-menu.label-name")}
    />
</div>
<div class="flex flex-col">
    {#if $search === ""}
        <FilterLabel
            label={{ kind: "allLabels" }}
            checked={$selected.kind === "allLabels"}
            on:checked={() => filterByLabel({ kind: "allLabels" })}
            on:unchecked={() => unfilterByLabel({ kind: "allLabels" })}
        />
        <FilterLabel
            label={{ kind: "noLabel" }}
            checked={$selected.kind === "noLabel"}
            on:checked={() => filterByLabel({ kind: "noLabel" })}
            on:unchecked={() => unfilterByLabel({ kind: "noLabel" })}
        />
    {/if}
    {#each $searchResults as label (label.uuid)}
        <FilterLabel
            label={{ kind: "label", label }}
            checked={$selected.kind === "labels"
                ? $selected.labelUuids.has(label.uuid)
                : false}
            {canEdit}
            on:checked={() =>
                filterByLabel({ kind: "label", labelUuid: label.uuid })}
            on:unchecked={() =>
                unfilterByLabel({ kind: "label", labelUuid: label.uuid })}
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
