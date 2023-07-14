<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Briefcase } from "@steeze-ui/heroicons";
    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import Filter from "$lib/figma/dropdown/Filter.svelte";
    import type { ContextMenuType } from "$lib/types/ui";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let open = true;

    let sideNavContextMenuAnchor: HTMLElement;
    let workspaceContextMenuAnchor: HTMLElement;

    let sideNavContextMenuType: ContextMenuType;
    $: sideNavContextMenuType = {
        kind: "sideNav" as const,
        workspace,
    };

    function showSideNavContextMenu() {
        openContextMenu(sideNavContextMenuType, sideNavContextMenuAnchor);
    }

    let workspaceContextMenuType: ContextMenuType;
    $: workspaceContextMenuType = {
        kind: "workspace",
    };

    function showWorkspaceContextMenu() {
        openContextMenu(workspaceContextMenuType, workspaceContextMenuAnchor);
    }
</script>

{#if open}
    <div class="px-4 pb-4">
        <div class="flex flex-row items-center justify-between">
            <div bind:this={workspaceContextMenuAnchor}>
                <Filter
                    icon={Briefcase}
                    label={$_("workspace-menu.workspace")}
                    open={false}
                    on:click={showWorkspaceContextMenu}
                />
            </div>
            <div
                class="flex flex-row items-center"
                bind:this={sideNavContextMenuAnchor}
            >
                <WorkspaceSettings on:click={showSideNavContextMenu} />
            </div>
        </div>
    </div>
{:else}
    <div class="flex flex-col items-center justify-between gap-4">
        <div bind:this={workspaceContextMenuAnchor}>
            <BorderedIcon
                type="workspace"
                on:click={showWorkspaceContextMenu}
            />
        </div>
        <div bind:this={sideNavContextMenuAnchor}>
            <WorkspaceSettings on:click={showSideNavContextMenu} />
        </div>
    </div>
{/if}
