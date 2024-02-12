<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
    import { Folder, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import Loading from "$lib/components/loading.svelte";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SelectWorkspaceBoard from "$lib/figma/buttons/SelectWorkspaceBoard.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import {
        boardExpandOpen,
        toggleBoardExpandOpen,
    } from "$lib/stores/dashboard";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";
    import { getArchiveUrl } from "$lib/urls";

    export let workspace: Workspace;

    async function openCreateWorkspaceBoard() {
        const target = {
            kind: "createWorkspaceBoard" as const,
            workspace,
        };
        await openConstructiveOverlay(target);
    }
</script>

<SideNavMenuCategory
    label={$_("dashboard.boards")}
    icon={Folder}
    open={$boardExpandOpen}
    on:click={toggleBoardExpandOpen}
    filtered={false}
/>
{#if $boardExpandOpen}
    <div class="flex shrink flex-col overflow-y-auto">
        {#if workspace.workspace_boards === undefined}
            <Loading />
        {:else if workspace.workspace_boards.length === 0}
            <div class="flex flex-col gap-2 p-4">
                <p>
                    {$_("dashboard.side-nav.workspace-boards.empty.message")}
                </p>
                <p>
                    <Anchor
                        label={$_(
                            "dashboard.side-nav.workspace-boards.empty.archive",
                        )}
                        href={getArchiveUrl(workspace.uuid)}
                        size="normal"
                    />
                </p>
            </div>
        {:else}
            {#each workspace.workspace_boards as workspaceBoard (workspaceBoard.uuid)}
                <SelectWorkspaceBoard {workspace} {workspaceBoard} />
            {/each}
        {/if}
    </div>
    <ContextMenuButton
        label={$_("dashboard.create-board")}
        icon={Plus}
        color="primary"
        state="normal"
        kind={{ kind: "button", action: openCreateWorkspaceBoard }}
    />
{/if}
