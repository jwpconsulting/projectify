<script lang="ts">
    import LabelDropdownClosedNav from "$lib/figma/buttons/LabelDropdownClosedNav.svelte";
    import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";
    import WorkspaceSelector from "$lib/figma/navigation/side-nav/WorkspaceSelector.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        selectWorkspaceBoardUuid,
        showFilters,
    } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    export let workspaces: Workspace[];
    export let workspace: Workspace;
</script>

<nav class="inline-flex h-full flex-col items-center gap-12 bg-foreground p-4">
    <div class="flex flex-col items-center justify-between">
        <div class="flex flex-col items-center gap-12">
            <div
                class="flex flex-col items-center gap-6 border-b border-border pb-12"
            >
                <WorkspaceSelector {workspaces} {workspace} open={false} />
                <div class="flex flex-col items-center gap-6">
                    <div class="flex flex-col items-center gap-4">
                        {#if workspace.workspace_boards}
                            {#each workspace.workspace_boards as board}
                                <SquovalIcon
                                    icon="board"
                                    state="active"
                                    action={{
                                        kind: "a",
                                        href: getDashboardWorkspaceBoardUrl(
                                            board.uuid,
                                        ),
                                        onInteract() {
                                            selectWorkspaceBoardUuid(
                                                workspace.uuid,
                                                board.uuid,
                                            );
                                        },
                                    }}
                                />
                            {/each}
                        {/if}
                    </div>
                </div>
            </div>
            {#if $showFilters}
                <div class="flex flex-col gap-8">
                    <div class="flex flex-col items-center gap-6">
                        <UserDropdownClosedNav />
                        <LabelDropdownClosedNav />
                    </div>
                </div>
            {/if}
        </div>
    </div>
</nav>
