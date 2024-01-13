<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { Briefcase, ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import BorderedIcon from "$lib/figma/buttons/BorderedIcon.svelte";
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

    let workspaceContextMenuOpen = false;

    async function showWorkspaceContextMenu() {
        workspaceContextMenuOpen = true;
        try {
            await openContextMenu(
                workspaceContextMenuType,
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
                    on:click={showWorkspaceContextMenu}
                    class="flex w-full flex-row items-center justify-between gap-2 rounded-lg border border-border p-2 hover:bg-secondary-hover"
                >
                    <div class="flex min-w-0 flex-row items-center gap-2">
                        <Icon
                            src={Briefcase}
                            theme="outline"
                            class="h-4 w-4 shrink-0"
                        />
                        <div class="min-w-0 truncate text-sm font-bold">
                            {workspace.title}
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
