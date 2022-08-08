<script lang="ts">
    import { _ } from "svelte-i18n";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import { getDropDown } from "$lib/components/globalDropDown.svelte";
    import type { DropDownMenuItem } from "$lib/components/globalDropDown.svelte";
    import EllipsisSideNav from "$lib/figma/EllipsisSideNav.svelte";
    import IconArchive from "$lib/components/icons/icon-archive.svelte";
    import IconSettings from "$lib/components/icons/icon-settings.svelte";
    import IconTag from "$lib/components/icons/icon-tag.svelte";
    import { getSettingsUrl, getArchiveUrl } from "$lib/urls";
    import Filter from "$lib/figma/Filter.svelte";
    import { Briefcase } from "@steeze-ui/heroicons";
    let dropDownMenuBtnRef: HTMLElement;

    function openDropDownMenu() {
        if (!$currentWorkspace) {
            console.error("Expected $currentWorkspace");
            return;
        }
        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("edit-labels"),
                icon: IconTag,
                href: getSettingsUrl($currentWorkspace.uuid, "labels"),
            },
            {
                label: $_("Archive"),
                icon: IconArchive,
                href: getArchiveUrl($currentWorkspace.uuid),
            },
            {
                label: $_("settings"),
                icon: IconSettings,
                href: getSettingsUrl($currentWorkspace.uuid, "index"),
            },
        ];
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, dropDownMenuBtnRef);
    }
</script>

<div class="px-4 pb-4">
    <div class="flex flex-row items-center justify-between">
        <Filter
            icon={Briefcase}
            label={$_("workspace-menu.workspace")}
            open={false}
        />
        <div bind:this={dropDownMenuBtnRef}>
            <EllipsisSideNav on:click={openDropDownMenu} />
        </div>
    </div>
</div>
