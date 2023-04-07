<script lang="ts">
    import Filter from "$lib/figma/dropdown/Filter.svelte";
    import HelpDropdownButton from "$lib/figma/dropdown/HelpDropdownButton.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
    import HelpDropdownMenu from "$lib/figma/dropdown/HelpDropdownMenu.svelte";
    import { Tag } from "@steeze-ui/heroicons";
    import { falseTrue, fr } from "$lib/storybook";
</script>

List Value
<div class={fr}>
    {#each falseTrue as open}
        <Filter icon={Tag} label="Filter by labels" {open} />
    {/each}
</div>

Help Dropdown States
<div class={fr}>
    {#each falseTrue as open}
        <HelpDropdownButton label="Help Sections" {open} />
    {/each}
</div>

Help Dropdown Menu
<div>
    <HelpDropdownMenu />
</div>

Help Dropdown
<div class={fr}>
    {#each falseTrue as open}
        <div class="/">
            <HelpDropdown {open} />
        </div>
    {/each}
</div>
