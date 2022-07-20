<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getDropDown } from "../globalDropDown.svelte";
    import type { DropDownMenuItem } from "../globalDropDown.svelte";
    import IconArchive from "../icons/icon-archive.svelte";
    import IconSettings from "../icons/icon-settings.svelte";
    import IconTag from "../icons/icon-tag.svelte";
    import SideNavBoards from "./SideNavBoards.svelte";
    import SideNavMembers from "./SideNavMembers.svelte";
    import SideNavLabels from "./SideNavLabels.svelte";
    import SideNavBulkSelect from "./SideNavBulkSelect.svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import {
        Briefcase,
        ChevronDown,
        DotsHorizontal,
    } from "@steeze-ui/heroicons";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import {} from "$lib/stores/dashboard";

    let dropDownMenuBtnRef: HTMLElement;
    function openDropDownMenu() {
        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("edit-labels"),
                icon: IconTag,
                href: `/dashboard/settings/${
                    $currentWorkspace ? $currentWorkspace.uuid : ""
                }?tab=labels`,
            },
            {
                label: $_("Archive"),
                icon: IconArchive,
                href: `/dashboard/archive/${
                    $currentWorkspace ? $currentWorkspace.uuid : ""
                }`,
            },
            {
                label: $_("settings"),
                icon: IconSettings,
                href: `/dashboard/settings/${
                    $currentWorkspace ? $currentWorkspace.uuid : ""
                }`,
            },
        ];
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, dropDownMenuBtnRef);
    }
</script>

<nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
    <div class="px-4 pb-4">
        <div class="flex flex-row items-center justify-between">
            <div
                class="flex w-[151px] items-center justify-between rounded-lg border border-base-300 p-2"
            >
                <Icon src={Briefcase} theme="outline" class="h-6 w-6" />
                <div class="text-bold text-sm">Workspace</div>
                <Icon src={ChevronDown} theme="outline" class="h-4 w-4" />
            </div>
            <button
                bind:this={dropDownMenuBtnRef}
                class="rounded-full border border-primary p-0.5"
                on:click={openDropDownMenu}
            >
                <Icon src={DotsHorizontal} class="h-5 w-5 text-primary" />
            </button>
        </div>
    </div>
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <SideNavBoards />
        <SideNavMembers />
        <SideNavLabels />
        <SideNavBulkSelect />
    </div>
</nav>
