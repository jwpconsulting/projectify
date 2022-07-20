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
    import { selectedLabels } from "$lib/stores/dashboard";

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
    let allSelected: boolean;
    let noneSelected: boolean;
    $: {
        if (defaultLabels.length > 0) {
            allSelected = $selectedLabels.size === defaultLabels.length;
            noneSelected = $selectedLabels.size === 0;
        }
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

    function selectLabel(label: Label | "all" | "none") {
        console.log(label);
        if (label === "all") {
            if (allSelected) {
                selectedLabels.clear();
            } else {
                labels.forEach((label) => {
                    selectedLabels.set(label.uuid, true);
                });
            }
        } else if (label === "none") {
            selectedLabels.clear();
        } else {
            const isSelected = $selectedLabels.get(label.uuid) === true;
            if (isSelected) {
                selectedLabels.del(label.uuid);
            } else {
                selectedLabels.set(label.uuid, true);
            }
        }
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
                selected={allSelected}
                onSelect={() => selectLabel("all")}
                editable={false}
            />
            <FilterLabel
                label={"none"}
                selected={noneSelected}
                onSelect={() => selectLabel("none")}
            />
        {/if}
        {#each labels as label (label.uuid)}
            <FilterLabel
                {label}
                selected={$selectedLabels.get(label.uuid) === true}
                onSelect={() => selectLabel(label)}
                editable={true}
            />
        {/each}
    </div>
{/if}
