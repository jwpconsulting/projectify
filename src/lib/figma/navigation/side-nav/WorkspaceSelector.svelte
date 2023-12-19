<script lang="ts">
    import { Briefcase } from "@steeze-ui/heroicons";

    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
    import Filter from "$lib/figma/dropdown/Filter.svelte";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let workspaces: Workspace[];
    export let open: boolean;

    let sideNavContextMenuAnchor: HTMLElement;
    let workspaceContextMenuAnchor: HTMLElement;

    let sideNavContextMenuType: ContextMenuType;
    $: sideNavContextMenuType = {
        kind: "sideNav" as const,
        workspace,
    };

    async function showSideNavContextMenu() {
        await openContextMenu(
            sideNavContextMenuType,
            sideNavContextMenuAnchor,
        );
    }

    let workspaceContextMenuType: ContextMenuType;
    $: workspaceContextMenuType = {
        kind: "workspace",
        workspaces,
    };

    async function showWorkspaceContextMenu() {
        await openContextMenu(
            workspaceContextMenuType,
            workspaceContextMenuAnchor,
        );
    }
</script>

{#if open}
    <div class="px-4 pb-4">
        <div class="flex flex-row items-center justify-between gap-4">
            <div class="min-w-0" bind:this={workspaceContextMenuAnchor}>
                <Filter
                    icon={Briefcase}
                    label={workspace.title}
                    open={false}
                    on:click={showWorkspaceContextMenu}
                />
            </div>
            <div bind:this={sideNavContextMenuAnchor}>
                <CircleIcon
                    icon="ellipsis"
                    size="medium"
                    action={{ kind: "button", action: showSideNavContextMenu }}
                />
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
            <CircleIcon
                icon="ellipsis"
                size="medium"
                action={{ kind: "button", action: showSideNavContextMenu }}
            />
        </div>
    </div>
{/if}
