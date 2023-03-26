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
    let workspaceContextMenuAnchor: HTMLElement;

    export let showWorkspaceContextMenu: (anchor: HTMLElement) => void;
</script>

<div class="px-4 pb-4">
    <div class="flex flex-row items-center justify-between">
        <div bind:this={workspaceContextMenuAnchor}>
            <Filter
                icon={Briefcase}
                label={$_("workspace-menu.workspace")}
                open={false}
                on:click={() =>
                    showWorkspaceContextMenu(workspaceContextMenuAnchor)}
            />
        </div>
        <div bind:this={dropDownMenuBtnRef}>
            <WorkspaceSettings />
        </div>
    </div>
</div>
