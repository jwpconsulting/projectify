<script lang="ts">
    import { _ } from "svelte-i18n";
    import SideNavMenuCategory from "./SideNavMenuCategory.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import type { Label } from "$lib/types";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import SearchField from "$lib/components/SearchField.svelte";
    import FilterLabel from "$lib/components/FilterLabel.svelte";
    import Fuse from "fuse.js";
    import { fuseSearchThreshold } from "$lib/stores/dashboard";
    import { selectedLabels, selectLabel } from "$lib/stores/dashboard";

    let open = true;

    let labels: Label[] = [];
    let searchInput: string = "";
    let defaultLabels: Label[];
    $: {
        defaultLabels = $currentWorkspace
            ? $currentWorkspace.labels || []
            : [];
        labels =
            searchInput === ""
                ? defaultLabels
                : search(defaultLabels, searchInput);
    }

    function search(labels: Label[], searchInput: string) {
        const searchEngine = new Fuse(labels, {
            keys: ["name"],
            threshold: fuseSearchThreshold,
            shouldSort: false,
        });
        const result = searchEngine.search(searchInput);
        return result.map((res: Fuse.FuseResult<Label>) => res.item);
    }
</script>

<SideNavMenuCategory label={$_("dashboard.labels")} icon={Tag} bind:open />
{#if open}
    <div class="flex flex-col px-4 pt-2 pb-4">
        <div class="p-2 text-xs font-bold capitalize">
            {$_("dashboard.filter-labels")}
        </div>
        <SearchField
            bind:searchInput
            placeholder={$_("dashboard.label-name")}
        />
    </div>
    <div class="flex flex-col">
        {#if searchInput === ""}
            <FilterLabel
                label={"all"}
                selected={$selectedLabels.kind === "allLabels"}
                onSelect={() => selectLabel({ kind: "allLabels" })}
                editable={false}
            />
            <FilterLabel
                label={"none"}
                selected={$selectedLabels.kind === "noLabel"}
                onSelect={() => selectLabel({ kind: "noLabel" })}
            />
        {/if}
        {#each labels as label (label.uuid)}
            <FilterLabel
                {label}
                selected={$selectedLabels.kind === "labels"
                    ? $selectedLabels.labelUuids.has(label.uuid)
                    : false}
                onSelect={() =>
                    selectLabel({ kind: "label", labelUuid: label.uuid })}
                editable={true}
            />
        {/each}
    </div>
{/if}
