<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { Briefcase, ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { currentWorkspaces } from "$lib/stores/dashboard/workspace";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { WorkspaceDetail } from "$lib/types/workspace";

    export let workspace: WorkspaceDetail | undefined = undefined;
    // TODO Rename to collapsed
    export let open: boolean;

    let sideNavContextMenuAnchor: HTMLElement;
    let workspaceContextMenuAnchor: HTMLElement;

    async function showSideNavContextMenu() {
        if (workspace === undefined) {
            throw new Error("Expected workspace");
        }
        await openContextMenu(
            {
                kind: "sideNav",
                workspace,
            },
            sideNavContextMenuAnchor,
        );
    }

    let workspaceContextMenuOpen = false;

    async function showWorkspaceContextMenu() {
        const workspaces = $currentWorkspaces;
        if (!workspaces) {
            throw new Error("Expected workspaces");
        }
        workspaceContextMenuOpen = true;
        try {
            await openContextMenu(
                {
                    kind: "workspace",
                    workspaces,
                },
                workspaceContextMenuAnchor,
            );
        } finally {
            workspaceContextMenuOpen = false;
        }
    }
</script>

{#if open}
    <div class="flex flex-col gap-2 px-4 pb-4">
        <div class="flex flex-row items-center justify-between gap-4">
            <div class="min-w-0 grow" bind:this={workspaceContextMenuAnchor}>
                <button
                    disabled={$currentWorkspaces === undefined}
                    on:click={showWorkspaceContextMenu}
                    class="flex w-full flex-row items-center justify-between gap-2 rounded-lg border border-border p-2 hover:bg-secondary-hover"
                >
                    <div class="flex min-w-0 flex-row items-center gap-2">
                        <Icon
                            src={Briefcase}
                            theme="outline"
                            class="h-4 w-4 shrink-0"
                        />
                        <div class="min-w-0 truncate font-bold">
                            {workspace
                                ? workspace.title
                                : $_(
                                      "dashboard.side-nav.workspace-selector.select",
                                  )}
                        </div>
                    </div>
                    <Icon
                        src={workspaceContextMenuOpen
                            ? ChevronUp
                            : ChevronDown}
                        theme="outline"
                        class="h-4 w-4 shrink-0"
                    />
                </button>
            </div>
            <div bind:this={sideNavContextMenuAnchor}>
                <CircleIcon
                    ariaLabel={$_(
                        "dashboard.side-nav.workspace-selector.context-menu",
                    )}
                    icon="ellipsis"
                    size="medium"
                    action={{
                        kind: "button",
                        action: showSideNavContextMenu,
                        disabled: workspace === undefined,
                    }}
                />
            </div>
        </div>
    </div>
{:else}
    <div class="flex flex-col items-center justify-between gap-4">
        <div bind:this={workspaceContextMenuAnchor}>
            <BorderedIcon
                ariaLabel={$_("dashboard.side-nav.workspace-selector.select")}
                type="workspace"
                on:click={$currentWorkspaces !== undefined
                    ? showWorkspaceContextMenu
                    : undefined}
            />
        </div>
        <div bind:this={sideNavContextMenuAnchor}>
            <CircleIcon
                icon="ellipsis"
                size="medium"
                action={{
                    kind: "button",
                    action: showSideNavContextMenu,
                    disabled: workspace === undefined,
                }}
                ariaLabel={$_("dashboard.side-nav.open-context-menu")}
            />
        </div>
    </div>
{/if}
