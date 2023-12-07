<script lang="ts">
    import { Folder, Plus } from "@steeze-ui/heroicons";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import { menuButtonColors, menuButtonStates } from "$lib/figma/types";
    import { falseTrue, fc, fr, users } from "$lib/storybook";
</script>

Notifications
<div class={fr}>
    {#each falseTrue as isActive}
        <NotificationButton on:click={console.log} {isActive} />
    {/each}
</div>
Menu button
<div class={`${fc} w-40`}>
    {#each menuButtonStates as state}
        {#each menuButtonColors as color}
            <ContextMenuButton
                {state}
                {color}
                kind={{ kind: "button", action: console.log }}
                icon={Plus}
                label={state}
            />
        {/each}
    {/each}
</div>
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

Side nav menu category
<div class={fc}>
    {#each falseTrue as open}
        <div class={fr}>
            {#each falseTrue as filtered}
                <div class="w-56">
                    <SideNavMenuCategory
                        label="boards"
                        {open}
                        {filtered}
                        icon={Folder}
                        contained={false}
                    />
                </div>
            {/each}
        </div>
    {/each}
</div>

Side nav menu category focus
<div class={fc}>
    {#each falseTrue as open}
        <div class={fr}>
            {#each falseTrue as filtered}
                <div class="w-56">
                    <SideNavMenuCategoryFocus
                        label="boards"
                        {open}
                        {filtered}
                        icon={Folder}
                    />
                </div>
            {/each}
        </div>
    {/each}
</div>
