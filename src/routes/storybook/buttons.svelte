<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/figma/buttons/Button.svelte";
    import SideMenuCreate from "$lib/figma/buttons/SideMenuCreate.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import AddUserButton from "$lib/figma/buttons/AddUserButton.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import CancelSearch from "$lib/figma/buttons/CancelSearch.svelte";
    import WatcherButton from "$lib/figma/buttons/WatcherButton.svelte";
    import NotificationRead from "$lib/figma/buttons/NotificationRead.svelte";
    import WorkspaceMenuBar from "$lib/figma/buttons/WorkspaceMenuBar.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import OnboardingSeats from "$lib/figma/buttons/OnboardingSeats.svelte";
    import DecrementSeats from "$lib/figma/buttons/DecrementSeats.svelte";
    import IncrementSeats from "$lib/figma/buttons/IncrementSeats.svelte";
    import SeatInput from "$lib/figma/buttons/SeatInput.svelte";
    import StepperComponent from "$lib/figma/buttons/StepperComponent.svelte";
    import Stepper from "$lib/figma/buttons/Stepper.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import SideNavMain from "$lib/figma/buttons/SideNavMain.svelte";
    import WorkspaceBoardIcon from "$lib/figma/buttons/WorkspaceBoardIcon.svelte";
    import Squoval from "$lib/figma/buttons/Squoval.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import Label from "$lib/figma/buttons/Label.svelte";
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import UserExpand from "$lib/figma/buttons/UserExpand.svelte";
    import LabelDropdownClosedNav from "$lib/figma/buttons/LabelDropdownClosedNav.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import SelectBoard from "$lib/figma/buttons/SelectBoard.svelte";
    import { currentStep } from "$lib/stores/onboarding";
    import { Plus, Folder } from "@steeze-ui/heroicons";
    import {
        buttonSizes,
        buttonColors,
        sideMenuCreateSizes,
        circleIconSizes,
        circleIconIcons,
        menuButtonStates,
        menuButtonColors,
        stepperPositions,
        stepperActiveStates,
        sideNavMainTypes,
        boardButtonStates,
        squovalIcons,
        squovalStates,
    } from "$lib/figma/types";
    import {
        fr,
        fc,
        trueFalse,
        falseTrue,
        buttonStyles,
        users,
        labels,
        workspaceBoard,
    } from "$lib/storybook";
    import { browser } from "$app/env";
    import { setFirstWorkspace } from "$lib/stores/dashboard";

    const onboardingSeats = [5, 10, 15, 20, 25];
    if (browser) {
        setFirstWorkspace();
    }
</script>

Buttons
<div class={fr}>
    {#each buttonStyles as style}
        <div class={fc}>
            <div class="capitalize">
                {style.kind}
                {#if style.kind === "tertiary"}
                    {#if style.icon === null}
                        no icon
                    {:else}
                        icon {style.icon.position}
                    {/if}
                {/if}
            </div>
            {#each buttonColors as color}
                <div class={fc}>
                    <div class="capitalize">
                        {color}
                    </div>
                    {#each buttonSizes as size}
                        <div class={fr}>
                            {#each trueFalse as disabled}
                                <Button
                                    on:click={console.log}
                                    {style}
                                    {size}
                                    {color}
                                    {disabled}
                                >
                                    {disabled ? "Disabled" : "Button"}
                                </Button>
                            {/each}
                        </div>
                    {/each}
                </div>
            {/each}
        </div>
    {/each}
</div>

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
Circle icons
<div class={fr}>
    {#each circleIconSizes as size}
        <div>
            <div class="capitalize">
                {size}
            </div>
            <div class={fc}>
                {#each circleIconIcons as icon}
                    <div class={fr}>
                        {#each trueFalse as disabled}
                            <CircleIcon
                                on:click={console.log}
                                {icon}
                                {disabled}
                                {size}
                            />
                        {/each}
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</div>
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
        <NotificationRead on:click={console.log} {isRead} />
    {/each}
</div>
Workspace menu bar
<div class={fr}>
    {#each falseTrue as active}
        <WorkspaceMenuBar href="/" label="Members" {active} />
    {/each}
</div>
Menu button
<div class={`${fc} w-40`}>
    {#each menuButtonStates as state}
        {#each menuButtonColors as color}
            <ContextMenuButton
                on:click={console.log}
                {state}
                {color}
                kind={{ kind: "button" }}
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
        <OnboardingSeats on:click={console.log} {seats} />
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
<SeatInput />
Stepper components
<div class={fr}>
    {#each stepperPositions as position}
        <div class={fc}>
            {#each stepperActiveStates as state}
                <StepperComponent {position} {state} on:click={console.log} />
            {/each}
        </div>
    {/each}
</div>
Stepper ({$currentStep})
<Stepper />
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
    {#each sideNavMainTypes as type}
        <SideNavMain {type} on:click={console.log} />
    {/each}
</div>
Board button
<div class={fr}>
    {#each boardButtonStates as state}
        <WorkspaceBoardIcon {state} on:click={console.log} />
    {/each}
</div>
Squoval
<div class={fc}>
    {#each squovalIcons as icon}
        <div class={fr}>
            {#each squovalStates as state}
                <Squoval {icon} {state} on:click={console.log} />
            {/each}
        </div>
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

Label v2
<div class={fr}>
    {#each labels as label}
        <div class={`${fc} items-center`}>
            <div class="capitalize">
                {label.kind === "applyLabel"
                    ? $_("label.apply-label")
                    : label.kind}
            </div>
            <Label {label} />
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

User expand
<UserExpand />

Label expand
<LabelDropdownClosedNav />

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

Select board
<div class="w-96">
    <SelectBoard {workspaceBoard} />
</div>
