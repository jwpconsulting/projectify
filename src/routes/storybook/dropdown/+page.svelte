<script lang="ts">
    import { Tag } from "@steeze-ui/heroicons";

    import Filter from "$lib/figma/dropdown/Filter.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
    import { falseTrue, fr } from "$lib/storybook";
</script>

List Value
<div class={fr}>
    {#each falseTrue as open}
        <Filter icon={Tag} label="Filter by labels" {open} />
    {/each}
</div>

Help Dropdown
<div class={fr}>
    <HelpDropdown />
</div>
