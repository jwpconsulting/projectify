<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";

    import type {
        LabelSearchModule,
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";
    import LabelDropdownClosedNav from "$lib/figma/buttons/LabelDropdownClosedNav.svelte";
    import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
    import type { ContextMenuType } from "$lib/types/ui";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";
    import { sideNavOpen } from "$lib/stores/dashboard";

    export let workspace: Workspace;
    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;
    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    export let labelSearchModule: LabelSearchModule;

    let workspaceContextMenuAnchor: HTMLElement;
    let sideNavContextMenuAnchor: HTMLElement;

    export let open = true;

    $: open = $sideNavOpen;

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
    <nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
        <WorkspaceMenu {showWorkspaceContextMenu} {showSideNavContextMenu} />
        <div class="flex flex-col overflow-x-auto overflow-y-scroll">
            <Boards {workspaceBoardSearchModule} />
            <Members {workspaceUserSearchModule} />
            <LabelDropdown {labelSearchModule} />
        </div>
    </nav>
{:else}
    <!-- Figma says 72px but we only have 64 or 80 (16, 29 rem respectively)-->
    <!-- Might we refactor this into something separate? -->
    <nav
        class="inline-flex h-full w-20 flex-col items-center gap-12 bg-foreground p-4"
    >
        <div class="flex flex-col items-center justify-between">
            <div class="flex flex-col items-center gap-12">
                <div
                    class="flex flex-col items-center gap-6 border-b border-border pb-12"
                    bind:this={sideNavContextMenuAnchor}
                >
                    <WorkspaceSettings on:click={showSideNavContextMenu} />
                    <div
                        class="flex flex-col items-center gap-6"
                        bind:this={workspaceContextMenuAnchor}
                    >
                        <BorderedIcon
                            type="workspace"
                            on:click={showWorkspaceContextMenu.bind(
                                null,
                                workspaceContextMenuAnchor
                            )}
                        />
                        <div class="flex flex-col items-center gap-4">
                            {#if workspace.workspace_boards}
                                {#each workspace.workspace_boards as board}
                                    <SquovalIcon
                                        icon="board"
                                        state="active"
                                        action={{
                                            kind: "a",
                                            href: getDashboardWorkspaceBoardUrl(
                                                board.uuid
                                            ),
                                        }}
                                    />
                                {/each}
                            {/if}
                        </div>
                    </div>
                </div>
                <div class="flex flex-col gap-8">
                    <div class="flex flex-col items-center gap-6">
                        <UserDropdownClosedNav {workspaceUserSearchModule} />
                        <LabelDropdownClosedNav {labelSearchModule} />
                    </div>
                </div>
            </div>
        </div>
    </nav>
{/if}
