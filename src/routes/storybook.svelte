<script lang="ts">
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
    import { Plus } from "@steeze-ui/heroicons";
    import {
        buttonStyles,
        buttonSizes,
        buttonColors,
        circleIconSizes,
        circleIconIcons,
        menuButtonStates,
    } from "$lib/figma/types";
    import type { ButtonIcon } from "$lib/figma/types";

    const buttonTertiares: ButtonIcon[] = [
        { position: "left", icon: Plus },
        { position: "right", icon: Plus },
        null,
    ];
    const disabledStates = [true, false];
    const onboardingSeats = [5, 10, 15, 20, 25];
</script>

<div class="flex flex-col">
    Buttons
    <div class="flex flex-row flex-wrap">
        {#each buttonStyles as style}
            <div class="flex flex-col flex-wrap">
                <div class="capitalize">
                    {style}
                </div>
                {#each buttonColors as color}
                    <div class="flex flex-col flex-wrap">
                        <div class="capitalize">
                            {color}
                        </div>
                        {#each buttonSizes as size}
                            <div class="flex flex-row flex-wrap items-center">
                                {#if style == "tertiary"}
                                    {#each buttonTertiares as icon}
                                        <div class="capitalize">
                                            {icon ? icon.position : "no"}
                                        </div>
                                        <Button
                                            on:click={console.log}
                                            {style}
                                            {size}
                                            {color}
                                            disabled={false}
                                            {icon}
                                        >
                                            Button
                                        </Button>
                                    {/each}
                                {:else}
                                    {#each disabledStates as disabled}
                                        <Button
                                            on:click={console.log}
                                            {style}
                                            {size}
                                            {color}
                                            {disabled}
                                            icon={null}
                                        >
                                            {disabled ? "Disabled" : "Button"}
                                        </Button>
                                    {/each}
                                {/if}
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
    <div class="flex flex-row flex-wrap">
        {#each circleIconSizes as size}
            <div>
                <div class="capitalize">
                    {size}
                </div>
                <div class="flex flex-col flex-wrap">
                    {#each circleIconIcons as icon}
                        <div class="flex flex-row flex-wrap">
                            {#each disabledStates as disabled}
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
    <div class="flex flex-row">
        {#each disabledStates as isActive}
            <NotificationButton on:click={console.log} isActive={!isActive} />
        {/each}
    </div>
    Cancel search
    <div class="flex flex-row">
        {#each disabledStates as isActive}
            <CancelSearch on:click={console.log} isActive={!isActive} />
        {/each}
    </div>
    Watcher
    <div class="flex flex-row">
        {#each disabledStates as isActive}
            <WatcherButton on:click={console.log} isActive={!isActive} />
        {/each}
    </div>
    Notification read
    <div class="flex flex-row">
        {#each disabledStates as isRead}
            <NotificationRead on:click={console.log} isRead={!isRead} />
        {/each}
    </div>
    Workspace menu bar
    <WorkspaceMenuBar on:click={console.log}>members</WorkspaceMenuBar>
    Menu button
    <div class="flex w-40 flex-col">
        {#each menuButtonStates as state}
            <MenuButton
                on:click={console.log}
                {state}
                icon={Plus}
                label={state}
            />
        {/each}
    </div>
    Submenu dropdown
    <div class="flex w-40 flex-col">
        <SubMenuDropdown on:click={console.log} label="Button" icon={Plus} />
    </div>
    Onboarding seats
    <div class="flex flex-row flex-wrap gap-5">
        {#each onboardingSeats as seats}
            <OnboardingSeats on:click={console.log} {seats} />
        {/each}
    </div>
    Minus seats
    <div class="flex flex-row flex-wrap gap-5">
        {#each disabledStates as disabled}
            <MinusSeats on:click={console.log} {disabled} />
        {/each}
    </div>
    Add seats
    <AddSeats on:click={console.log} />
</div>
