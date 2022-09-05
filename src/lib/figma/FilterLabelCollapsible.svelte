<script lang="ts">
    import { _ } from "svelte-i18n";
    import SideNavMenuCategoryFocus from "$lib/figma/SideNavMenuCategoryFocus.svelte";
    import FilterLabelMenu from "$lib/figma/FilterLabelMenu.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import { selectedLabels } from "$lib/stores/dashboard";

    export let open: boolean = true;

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
    <FilterLabelMenu />
{/if}
