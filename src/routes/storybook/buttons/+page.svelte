<script lang="ts">
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import SideMenuCreate from "$lib/figma/buttons/SideMenuCreate.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import AddUserButton from "$lib/figma/buttons/AddUserButton.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import CancelSearch from "$lib/figma/buttons/CancelSearch.svelte";
    import WatcherButton from "$lib/figma/buttons/WatcherButton.svelte";
    import ReadNotification from "$lib/figma/buttons/ReadNotification.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import SelectSeats from "$lib/figma/buttons/SelectSeats.svelte";
    import DecrementSeats from "$lib/figma/buttons/DecrementSeats.svelte";
    import IncrementSeats from "$lib/figma/buttons/IncrementSeats.svelte";
    import SeatInputStepper from "$lib/figma/buttons/SeatInputStepper.svelte";
    import StepperVariant from "$lib/figma/buttons/StepperVariant.svelte";
    import ProgressStepper from "$lib/figma/buttons/ProgressStepper.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
    import WorkspaceBoardIcon from "$lib/figma/buttons/WorkspaceBoardIcon.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import { currentStep } from "$lib/stores/onboarding";
    import {
        boardButtonStates,
        borderedIconTypes,
        menuButtonColors,
        menuButtonStates,
        sideMenuCreateSizes,
        stepperActiveStates,
        stepperPositions,
    } from "$lib/figma/types";
    import { falseTrue, fc, fr, trueFalse, users } from "$lib/storybook";
    import { browser } from "$app/environment";
    import { setFirstWorkspace } from "$lib/stores/dashboard";

    const onboardingSeats = [5, 10, 15, 20, 25];
    if (browser) {
        setFirstWorkspace();
    }
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

Upload avatar
<UploadAvatar on:click={console.log} />
Add user
<AddUserButton on:click={console.log} />
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
Watcher
<div class={fr}>
    {#each falseTrue as isActive}
        <WatcherButton on:click={console.log} {isActive} />
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
Onboarding seats
<div class={fr}>
    {#each onboardingSeats as seats}
        <SelectSeats on:click={console.log} {seats} />
    {/each}
</div>
Minus seats
<div class={fr}>
    {#each trueFalse as disabled}
        <DecrementSeats on:click={console.log} {disabled} />
    {/each}
</div>
Add seats
<IncrementSeats on:click={console.log} />
Seat input
<SeatInputStepper />
Stepper components
<div class={fr}>
    {#each stepperPositions as position}
        <div class={fc}>
            {#each stepperActiveStates as state}
                <StepperVariant {position} {state} on:click={console.log} />
            {/each}
        </div>
    {/each}
</div>
Stepper ({$currentStep})
<ProgressStepper />
Mobile Menu
<div class={fr}>
    {#each falseTrue as isActive}
        <HamburgerMenu {isActive} on:click={console.log} />
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

Avatar with hover
<div class={fr}>
    {#each users as user}
        <div class={fc}>
            {user ? user.email : "No user"}
            <UserAccount
                {user}
                on:click={() => console.log("UserAccount", user)}
            />
        </div>
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
