<script lang="ts">
    import { _ } from "svelte-i18n";
    import SideNavMenuCategoryFocus from "$lib/figma/SideNavMenuCategoryFocus.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import SearchField from "$lib/components/SearchField.svelte";
    import FilterLabel from "$lib/figma/FilterLabel.svelte";
    import {
        selectedLabels,
        selectLabel,
        labelSearch,
        labelSearchResults,
    } from "$lib/stores/dashboard";

    let open = true;

    function toggleOpen() {
        open = !open;
    }
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleOpen}
    {open}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if open}
    <div class="flex flex-col px-4 pt-2 pb-4">
        <div class="p-2 text-xs font-bold capitalize">
            {$_("dashboard.filter-labels")}
        </div>
        <SearchField
            bind:searchInput={$labelSearch}
            placeholder={$_("dashboard.label-name")}
        />
    </div>
    <div class="flex flex-col">
        {#if $labelSearch === ""}
            <FilterLabel
                label={{ kind: "allLabels" }}
                selected={$selectedLabels.kind === "allLabels"}
                on:click={() => selectLabel({ kind: "allLabels" })}
            />
            <FilterLabel
                label={{ kind: "noLabel" }}
                selected={$selectedLabels.kind === "noLabel"}
                on:click={() => selectLabel({ kind: "noLabel" })}
            />
        {/if}
        {#each $labelSearchResults as label (label.uuid)}
            <FilterLabel
                label={{ kind: "label", label }}
                selected={$selectedLabels.kind === "labels"
                    ? $selectedLabels.labelUuids.has(label.uuid)
                    : false}
                on:click={() =>
                    selectLabel({ kind: "label", labelUuid: label.uuid })}
            />
        {/each}
    </div>
{/if}
