<script lang="ts">
    // Rename to figma/navigation/side-nav/Labels.svelte
    import { Tag } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard";
    import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
</script>

<SideNavMenuCategory
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleLabelDropdownClosedNavOpen}
    open={$labelExpandOpen}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if $labelExpandOpen}
    <div class="shrink overflow-y-auto">
        <LabelMenu />
    </div>
{/if}
