<script lang="ts">
    import { _ } from "svelte-i18n";
    import HelpDropdownButton from "$lib/figma/dropdown/HelpDropdownButton.svelte";
    import HelpDropdownMenu from "$lib/figma/dropdown/HelpDropdownMenu.svelte";

    export let open = true;

    function toggleOpen() {
        open = !open;
    }
</script>

<div class="flex flex-col">
    <HelpDropdownButton
        label={$_("help.help-sections")}
        on:click={toggleOpen}
        {open}
    />
    {#if open}
        <HelpDropdownMenu />
    {/if}
</div>
