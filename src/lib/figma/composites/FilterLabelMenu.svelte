<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { LabelSearchModule } from "$lib/types/stores";

    export let labelSearchModule: LabelSearchModule;
    export let canEdit = true;

    let { select, deselect, selected, search, searchResults } =
        labelSearchModule;

    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
</script>

<div class="flex flex-col px-4 pt-2 pb-4">
    <div class="p-2 text-xs font-bold first-letter:capitalize">
        {$_("dashboard.filter-labels")}
    </div>
    <InputField
        bind:value={$search}
        style={{ kind: "search" }}
        name="label-name"
        placeholder={$_("dashboard.label-name")}
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
</div>
