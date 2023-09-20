<script lang="ts">
    import { Tag } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard";
    import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleLabelDropdownClosedNavOpen}
    open={$labelExpandOpen}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if $labelExpandOpen}
    <LabelMenu />
{/if}
