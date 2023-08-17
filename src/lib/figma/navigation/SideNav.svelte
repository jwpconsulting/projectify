<script lang="ts">
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    import LabelDropdownClosedNav from "$lib/figma/buttons/LabelDropdownClosedNav.svelte";
    import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import type {
        LabelSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[];
    export let workspace: Workspace;
    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    export let labelSearchModule: LabelSearchModule;

    export let open = true;
</script>

{#if open}
    <nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
        <WorkspaceMenu {workspaces} {workspace} {open} />
        <div class="flex flex-col overflow-x-auto overflow-y-scroll">
            <Boards {workspace} />
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
                >
                    <WorkspaceMenu {workspaces} {workspace} {open} />
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
