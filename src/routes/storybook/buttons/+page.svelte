<script lang="ts">
    import { Plus } from "@steeze-ui/heroicons";

    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import { falseTrue, fc, fr, users } from "$lib/storybook";
</script>

Submenu dropdown
<div class={`${fc} w-40`}>
    <SubMenuDropdown on:click={console.log} label="Button" icon={Plus} />
</div>

Mobile search menu
<SearchMobile on:click={console.log} />

Filter user avatar
<div class={fc}>
    {#each users as user}
        <div class={fr}>
            {#each falseTrue as active}
                <SelectUserClosedNav {active} {user} />
            {/each}
        </div>
    {/each}
</div>
