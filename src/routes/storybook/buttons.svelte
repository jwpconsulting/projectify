<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/figma/Button.svelte";
    import EllipsisSideNav from "$lib/figma/EllipsisSideNav.svelte";
    import CircleIcon from "$lib/figma/CircleIcon.svelte";
    import UploadAvatar from "$lib/figma/UploadAvatar.svelte";
    import AddUserButton from "$lib/figma/AddUserButton.svelte";
    import NotificationButton from "$lib/figma/NotificationButton.svelte";
    import CancelSearch from "$lib/figma/CancelSearch.svelte";
    import WatcherButton from "$lib/figma/WatcherButton.svelte";
    import NotificationRead from "$lib/figma/NotificationRead.svelte";
    import WorkspaceMenuBar from "$lib/figma/WorkspaceMenuBar.svelte";
    import MenuButton from "$lib/figma/MenuButton.svelte";
    import SubMenuDropdown from "$lib/figma/SubMenuDropdown.svelte";
    import OnboardingSeats from "$lib/figma/OnboardingSeats.svelte";
    import MinusSeats from "$lib/figma/MinusSeats.svelte";
    import AddSeats from "$lib/figma/AddSeats.svelte";
    import SeatInput from "$lib/figma/SeatInput.svelte";
    import StepperComponent from "$lib/figma/StepperComponent.svelte";
    import Stepper from "$lib/figma/Stepper.svelte";
    import MobileMenu from "$lib/figma/MobileMenu.svelte";
    import MobileSearchMenu from "$lib/figma/MobileSearchMenu.svelte";
    import SideNavMain from "$lib/figma/SideNavMain.svelte";
    import BoardButton from "$lib/figma/BoardButton.svelte";
    import Squoval from "$lib/figma/Squoval.svelte";
    import AvatarWithHover from "$lib/figma/AvatarWithHover.svelte";
    import SelectLabelColor from "$lib/figma/SelectLabelColor.svelte";
    import SelectLabelFocus from "$lib/figma/SelectLabelFocus.svelte";
    import Label from "$lib/figma/Label.svelte";
    import FilterUserAvatar from "$lib/figma/FilterUserAvatar.svelte";
    import UserExpand from "$lib/figma/UserExpand.svelte";
    import LabelExpand from "$lib/figma/LabelExpand.svelte";
    import SideNavMenuCategory from "$lib/figma/SideNavMenuCategory.svelte";
    import SideNavMenuCategoryFocus from "$lib/figma/SideNavMenuCategoryFocus.svelte";
    import { currentStep } from "$lib/stores/onboarding";
    import { Plus, Folder } from "@steeze-ui/heroicons";
    import {
        buttonSizes,
        buttonColors,
        circleIconSizes,
        circleIconIcons,
        menuButtonStates,
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
        selectLabels,
        labels,
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
Ellipsis side nav
<EllipsisSideNav on:click={console.log} />
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
<WorkspaceMenuBar on:click={console.log}>members</WorkspaceMenuBar>
Menu button
<div class={`${fc} w-40`}>
    {#each menuButtonStates as state}
        <MenuButton on:click={console.log} {state} icon={Plus} label={state} />
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
        <MinusSeats on:click={console.log} {disabled} />
    {/each}
</div>
Add seats
<AddSeats on:click={console.log} />
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
        <MobileMenu {isActive} on:click={console.log} />
    {/each}
</div>
Mobile search menu
<MobileSearchMenu on:click={console.log} />
Side nav main
<div class={fr}>
    {#each sideNavMainTypes as type}
        <SideNavMain {type} on:click={console.log} />
    {/each}
</div>
Board button
<div class={fr}>
    {#each boardButtonStates as state}
        <BoardButton {state} on:click={console.log} />
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
            <AvatarWithHover
                {user}
                on:click={() => console.log("AvatarWithHover", user)}
            />
        </div>
    {/each}
</div>
Select label color
<div class={fr}>
    {#each selectLabels as label}
        <div class={`${fc} items-center`}>
            <div class="capitalize">
                {#if label.kind === "allLabels"}
                    all labels
                {:else if label.kind === "noLabel"}
                    no label
                {:else}
                    {label.label.name}
                {/if}
            </div>
            {#each falseTrue as active}
                <SelectLabelColor {label} {active} />
            {/each}
        </div>
    {/each}
</div>

Select label focus
<div class={fr}>
    {#each selectLabels as label}
        <div class={`${fc} items-center`}>
            <div class="capitalize">
                {#if label.kind === "allLabels"}
                    all labels
                {:else if label.kind === "noLabel"}
                    no label
                {:else}
                    {label.label.name}
                {/if}
            </div>
            {#each falseTrue as active}
                <SelectLabelFocus {label} {active} />
            {/each}
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
                <FilterUserAvatar {active} {user} />
            {/each}
        </div>
    {/each}
</div>

User expand
<UserExpand />

Label expand
<LabelExpand />

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
