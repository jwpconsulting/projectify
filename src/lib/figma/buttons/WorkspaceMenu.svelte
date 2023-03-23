<script lang="ts">
    import { _ } from "svelte-i18n";
    import { getDropDown } from "$lib/components/globalDropDown.svelte";
    import type { DropDownMenuItem } from "$lib/components/globalDropDown.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import IconArchive from "$lib/components/icons/icon-archive.svelte";
    import IconSettings from "$lib/components/icons/icon-settings.svelte";
    import IconTag from "$lib/components/icons/icon-tag.svelte";
    import { getSettingsUrl, getArchiveUrl } from "$lib/urls";
    import Filter from "$lib/figma/dropdown/Filter.svelte";
    import { Briefcase } from "@steeze-ui/heroicons";
    import type { WorkspaceSearchModule } from "$lib/types/stores";

    let dropDownMenuBtnRef: HTMLElement;

    export let workspaceSearchModule: WorkspaceSearchModule;

    let { currentWorkspace } = workspaceSearchModule;

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
            <WorkspaceSettings on:click={openDropDownMenu} />
        </div>
    </div>
</div>
