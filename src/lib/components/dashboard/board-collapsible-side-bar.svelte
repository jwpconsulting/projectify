<script lang="ts">
    import { boardSideBarOpen } from "$lib/stores/dashboard-ui";

    import { _ } from "svelte-i18n";

    import { getDropDown } from "../globalDropDown.svelte";
    import type { DropDownMenuItem } from "../globalDropDown.svelte";
    import IconArchive from "../icons/icon-archive.svelte";
    import IconArrowCircleLeft from "../icons/icon-arrow-circle-left.svelte";
    import IconArrowCircleRight from "../icons/icon-arrow-circle-right.svelte";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconSettings from "../icons/icon-settings.svelte";
    import IconTag from "../icons/icon-tag.svelte";
    import BoardsSideNav from "./boards-side-nav.svelte";
    import type { Workspace } from "$lib/types";

    export let selectedWorkspace: Workspace | null;
    export let selectedWorkspaceUUID: string | null;
    export let selectedBoardUUID: string | null;

    $: open = $boardSideBarOpen;

    let dropDownMenuBtnRef: HTMLElement;
    function openDropDownMenu() {
        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("minimise-sidebar"),
                icon: IconArrowCircleLeft,
                onClick: () => {
                    boardSideBarOpen.set(false);
                },
                hidden: open == false,
            },
            {
                label: $_("expand-sidebar"),
                icon: IconArrowCircleRight,
                onClick: () => {
                    boardSideBarOpen.set(true);
                },
                hidden: open == true,
            },

            {
                label: $_("edit-labels"),
                icon: IconTag,
                href: `/dashboard/settings/${selectedWorkspaceUUID}?tab=labels`,
            },
            {
                label: $_("Archive"),
                icon: IconArchive,
                href: `/dashboard/archive/${selectedWorkspaceUUID}`,
            },
            {
                label: $_("settings"),
                icon: IconSettings,
                href: `/dashboard/settings/${selectedWorkspaceUUID}`,
            },
        ];
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, dropDownMenuBtnRef);
    }
</script>

<nav
    class={`${
        open ? "w-60" : "w-14"
    } sticky top-0 flex min-h-full  shrink-0 flex-col overflow-hidden bg-base-100`}
>
    <!-- Tite and settings -->
    <div class="sticky top-0 z-50 flex bg-base-100 p-4">
        {#if open}
            <h1 class="grow text-xl font-bold capitalize">
                {selectedWorkspace ? selectedWorkspace.title : ""}
            </h1>
        {/if}
        <button
            bind:this={dropDownMenuBtnRef}
            on:click|stopPropagation={openDropDownMenu}
            class="btn btn-outline btn-primary btn-circle btn-xs shrink-0"
            ><IconMenu /></button
        >
    </div>

    <!-- Boards nav -->
    <div class:hidden={!open} class="flex grow flex-col overflow-hidden">
        {#if selectedWorkspaceUUID && selectedBoardUUID}
            <h2 class="p-4 text-base font-bold">Workspace Boards</h2>
            <BoardsSideNav {selectedWorkspaceUUID} {selectedBoardUUID} />
        {/if}
    </div>
</nav>
