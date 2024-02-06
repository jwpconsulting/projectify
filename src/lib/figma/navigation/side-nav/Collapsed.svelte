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

    export let workspaces: Workspace[] | undefined;
    export let workspace: Workspace | undefined;
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
                        {#if workspace?.workspace_boards}
                            {#each workspace.workspace_boards as board}
                                <SquovalIcon
                                    icon="board"
                                    state="active"
                                    action={{
                                        kind: "a",
                                        href: getDashboardWorkspaceBoardUrl(
                                            board.uuid,
                                        ),
                                        onInteract:
                                            selectWorkspaceBoardUuid.bind(
                                                null,
                                                workspace.uuid,
                                                board.uuid,
                                            ),
                                    }}
                                />
                            {/each}
                        {/if}
                    </div>
                </div>
            </div>
            {#if workspace !== undefined && $showFilters}
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
