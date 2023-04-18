<script lang="ts">
    import { _ } from "svelte-i18n";
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import type { FilterLabelMenuState } from "$lib/figma/types";
    import type { LabelSearchModule } from "$lib/types/stores";

    export let labelSearchModule: LabelSearchModule;

    export let state: FilterLabelMenuState = "list";
</script>

{#if state === "list"}
    <FilterLabelMenu {labelSearchModule} />
{:else}
    <div class="px-4 pt-2 pb-4">
        <div class="p-2 text-xs font-bold first-letter:capitalize">
            {$_("filter-label-menu.label-name")}
        </div>
    </div>
{/if}
