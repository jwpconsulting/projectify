<script lang="ts">
    import Filter from "$lib/figma/Filter.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import { fr, falseTrue } from "$lib/storybook";
</script>

List Value
<div class={fr}>
    {#each falseTrue as open}
        <Filter icon={Tag} label="Filter by labels" {open} />
    {/each}
</div>
