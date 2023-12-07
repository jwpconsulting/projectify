<script lang="ts">
    import { Folder, Plus } from "@steeze-ui/heroicons";

    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
    import CancelSearch from "$lib/figma/buttons/CancelSearch.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import ReadNotification from "$lib/figma/buttons/ReadNotification.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SideMenuCreate from "$lib/figma/buttons/SideMenuCreate.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import WorkspaceBoardIcon from "$lib/figma/buttons/WorkspaceBoardIcon.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import {
        boardButtonStates,
        borderedIconTypes,
        menuButtonColors,
        menuButtonStates,
        sideMenuCreateSizes,
    } from "$lib/figma/types";
    import { falseTrue, fc, fr, users } from "$lib/storybook";
</script>

Side menu create
<div class={fc}>
    {#each sideMenuCreateSizes as size}
        <SideMenuCreate
            on:click={console.log}
            {size}
            icon={Plus}
            label="Create New Label"
        />
    {/each}
</div>

Ellipsis side nav
<WorkspaceSettings on:click={console.log} />

Notifications
<div class={fr}>
    {#each falseTrue as isActive}
        <NotificationButton on:click={console.log} {isActive} />
    {/each}
</div>
Cancel search
<div class={fr}>
    {#each falseTrue as isActive}
        <CancelSearch on:click={console.log} {isActive} />
    {/each}
</div>
Notification read
<div class={fr}>
    {#each falseTrue as isRead}
        <ReadNotification on:click={console.log} {isRead} />
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
Mobile Menu
<div class={fr}>
    {#each falseTrue as isActive}
        <HamburgerMenu {isActive} action={console.log} />
    {/each}
</div>
Mobile search menu
<SearchMobile on:click={console.log} />

Side nav main
<div class={fr}>
    {#each borderedIconTypes as type}
        <BorderedIcon {type} on:click={console.log} />
    {/each}
</div>
Board button
<div class={fr}>
    {#each boardButtonStates as state}
        <WorkspaceBoardIcon {state} on:click={console.log} />
    {/each}
</div>

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
