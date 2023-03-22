<script lang="ts">
    import { _ } from "svelte-i18n";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import {
        selectLabel,
        deselectLabel,
        selectedLabels,
        labelSearch,
        labelSearchResults,
    } from "$lib/stores/dashboard";
    import type { LabelSearchModule } from "$lib/types/stores";

    export let open: boolean = true;

    function toggleOpen() {
        open = !open;
    }

    const labelSearchModule: LabelSearchModule = {
        select: selectLabel,
        deselect: deselectLabel,
        selected: selectedLabels,
        search: labelSearch,
        searchResults: labelSearchResults,
    };
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleOpen}
    {open}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if open}
    <LabelMenu {labelSearchModule} />
{/if}
