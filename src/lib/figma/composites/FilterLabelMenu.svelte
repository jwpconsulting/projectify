<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Plus } from "@steeze-ui/heroicons";

    import type { LabelSearchModule } from "$lib/types/stores";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";

    export let labelSearchModule: LabelSearchModule;
    export let canEdit = true;
    // If it is null, we don't show the create new label button
    export let startCreateLabel: (() => void) | null = null;

    let { select, deselect, selected, search, searchResults } =
        labelSearchModule;
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
            on:checked={() => select({ kind: "allLabels" })}
            on:unchecked={() => deselect({ kind: "allLabels" })}
        />
        <FilterLabel
            label={{ kind: "noLabel" }}
            checked={$selected.kind === "noLabel"}
            on:checked={() => select({ kind: "noLabel" })}
            on:unchecked={() => deselect({ kind: "noLabel" })}
        />
    {/if}
    {#each $searchResults as label (label.uuid)}
        <FilterLabel
            label={{ kind: "label", label }}
            checked={$selected.kind === "labels"
                ? $selected.labelUuids.has(label.uuid)
                : false}
            {canEdit}
            on:checked={() => select({ kind: "label", labelUuid: label.uuid })}
            on:unchecked={() =>
                deselect({ kind: "label", labelUuid: label.uuid })}
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
