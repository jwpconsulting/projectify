<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Tag } from "@steeze-ui/heroicons";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";
    import type { LabelSearchModule } from "$lib/types/stores";
    import type { FilterLabelMenuState } from "$lib/figma/types";

    export let labelSearchModule: LabelSearchModule;
    export let open = true;
    export let state: FilterLabelMenuState = "list";

    function toggleOpen() {
        open = !open;
    }

    let { selected } = labelSearchModule;

    function returnToList() {
        state = "list";
    }
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleOpen}
    {open}
    filtered={$selected.kind !== "allLabels"}
/>
{#if open}
    <LabelMenu
        {state}
        {labelSearchModule}
        cancelCreate={returnToList}
        savedLabel={returnToList}
    />
{/if}
