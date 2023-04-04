<script lang="ts">
    import { _ } from "svelte-i18n";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import type { LabelSearchModule } from "$lib/types/stores";

    export let labelSearchModule: LabelSearchModule;
    export let open = true;

    function toggleOpen() {
        open = !open;
    }

    let { selected } = labelSearchModule;
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleOpen}
    {open}
    filtered={$selected.kind !== "allLabels"}
/>
{#if open}
    <LabelMenu {labelSearchModule} />
{/if}
