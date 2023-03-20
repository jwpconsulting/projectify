<script lang="ts">
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import LabelMenu from "$lib/figma/composites/LabelMenu.svelte";

    import { setFirstWorkspace } from "$lib/stores/dashboard";
    import { browser } from "$app/environment";
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
            <LabelMenu {state} />
        </div>
    {/each}
</div>

Filter label collapsible
<div class={fr}>
    {#each falseTrue as open}
        <div class="w-96">
            <LabelDropdown {open} />
        </div>
    {/each}
</div>
