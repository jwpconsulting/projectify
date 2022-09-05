<script lang="ts">
    import FilterLabelCollapsible from "$lib/figma/FilterLabelCollapsible.svelte";
    import FilterLabelMenu from "$lib/figma/FilterLabelMenu.svelte";

    import { setFirstWorkspace } from "$lib/stores/dashboard";
    import { browser } from "$app/env";
    import { falseTrue, fr } from "$lib/storybook";
    import { filterLabelMenuStates } from "$lib/figma/types";

    if (browser) {
        setFirstWorkspace();
    }
</script>

Filter label menu
<div class={fr}>
    {#each filterLabelMenuStates as state}
        <div class="w-96">
            <FilterLabelMenu {state} />
        </div>
    {/each}
</div>

Filter label collapsible
<div class={fr}>
    {#each falseTrue as open}
        <div class="w-96">
            <FilterLabelCollapsible {open} />
        </div>
    {/each}
</div>
