<script lang="ts">
    import { _ } from "svelte-i18n";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import Filter from "$lib/figma/dropdown/Filter.svelte";
    import { Briefcase } from "@steeze-ui/heroicons";

    let dropDownMenuBtnRef: HTMLElement;
    let workspaceContextMenuAnchor: HTMLElement;

    export let showWorkspaceContextMenu: (anchor: HTMLElement) => void;
    export let showSideNavContextMenu: (anchor: HTMLElement) => void;
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
        <div class="flex flex-row items-center" bind:this={dropDownMenuBtnRef}>
            <WorkspaceSettings
                on:click={() => showSideNavContextMenu(dropDownMenuBtnRef)}
            />
        </div>
    </div>
</div>
