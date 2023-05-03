<script lang="ts">
    import WorkspaceMenu from "$lib/figma/buttons/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import LabelDropdown from "$lib/figma/composites/LabelDropdown.svelte";
    import WorkspaceSettings from "$lib/figma/buttons/WorkspaceSettings.svelte";
    import type {
        LabelSearchModule,
        SideNavModule,
        WorkspaceBoardSearchModule,
        WorkspaceUserSearchModule,
    } from "$lib/types/stores";
    import LabelDropdownClosedNav from "$lib/figma/buttons/LabelDropdownClosedNav.svelte";
    import UserDropdownClosedNav from "$lib/figma/buttons/UserDropdownClosedNav.svelte";

    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;
    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    export let labelSearchModule: LabelSearchModule;
    export let sideNavModule: SideNavModule;

    let dropDownMenuBtnRef: HTMLElement;

    export let open = true;

    let { showWorkspaceContextMenu, showSideNavContextMenu } = sideNavModule;
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
    <nav class="inline-flex h-full flex-col gap-12 bg-foreground p-4">
        <div class="flex flex-col justify-between">
            <div>
                <div class="flex flex-col gap-6 border-b border-border pb-12">
                    <WorkspaceSettings
                        on:click={showSideNavContextMenu.bind(
                            null,
                            dropDownMenuBtnRef
                        )}
                    />
                    <div>TODO Boards</div>
                </div>
                <div class="flex flex-col gap-8">
                    <div>BorderedIcon</div>
                    <div class="flex flex-col gap-6">
                        <UserDropdownClosedNav {workspaceUserSearchModule} />
                        <LabelDropdownClosedNav {labelSearchModule} />
                    </div>
                </div>
            </div>
        </div>
    </nav>
{/if}
