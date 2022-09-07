<script lang="ts">
    import { _ } from "svelte-i18n";
    import InputField from "$lib/figma/InputField.svelte";
    import FilterLabel from "$lib/figma/FilterLabel.svelte";
    import {
        selectedLabels,
        deselectLabel,
        selectLabel,
        labelSearch,
        labelSearchResults,
    } from "$lib/stores/dashboard";
    import type { FilterLabelMenuState } from "$lib/figma/types";

    export let state: FilterLabelMenuState = "list";
</script>

{#if state === "list"}
    <div class="flex flex-col px-4 pt-2 pb-4">
        <div class="p-2 text-xs font-bold first-letter:capitalize">
            {$_("dashboard.filter-labels")}
        </div>
        <InputField
            bind:value={$labelSearch}
            style="search"
            placeholder={$_("dashboard.label-name")}
        />
    </div>
    <div class="flex flex-col">
        {#if $labelSearch === ""}
            <FilterLabel
                label={{ kind: "allLabels" }}
                checked={$selectedLabels.kind === "allLabels"}
                on:checked={() => selectLabel({ kind: "allLabels" })}
                on:unchecked={() => deselectLabel({ kind: "allLabels" })}
            />
            <FilterLabel
                label={{ kind: "noLabel" }}
                checked={$selectedLabels.kind === "noLabel"}
                on:checked={() => selectLabel({ kind: "noLabel" })}
                on:unchecked={() => deselectLabel({ kind: "noLabel" })}
            />
        {/if}
        {#each $labelSearchResults as label (label.uuid)}
            <FilterLabel
                label={{ kind: "label", label }}
                checked={$selectedLabels.kind === "labels"
                    ? $selectedLabels.labelUuids.has(label.uuid)
                    : false}
                on:checked={() =>
                    selectLabel({ kind: "label", labelUuid: label.uuid })}
                on:unchecked={() =>
                    deselectLabel({ kind: "label", labelUuid: label.uuid })}
            />
        {/each}
    </div>
{:else}
    <div class="px-4 pt-2 pb-4">
        <div class="p-2 text-xs font-bold first-letter:capitalize">
            {$_("filter-label-menu.label-name")}
        </div>
    </div>
{/if}
