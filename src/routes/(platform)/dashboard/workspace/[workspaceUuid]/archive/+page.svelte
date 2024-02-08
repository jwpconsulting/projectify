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
    import parseISO from "date-fns/parseISO";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        archiveWorkspaceBoard,
        deleteWorkspaceBoard,
    } from "$lib/repository/workspace/workspaceBoard";
    import { currentArchivedWorkspaceBoards } from "$lib/stores/dashboard";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    $: archivedWorkspaceBoards = $currentArchivedWorkspaceBoards ?? [];

    async function recoverAction(workspaceBoard: WorkspaceBoard) {
        await openConstructiveOverlay({
            kind: "recoverWorkspaceBoard",
            workspaceBoard,
        });
        await archiveWorkspaceBoard(workspaceBoard, false, { fetch });
    }

    async function deleteAction(workspaceBoard: WorkspaceBoard) {
        await openDestructiveOverlay({
            kind: "deleteWorkspaceBoard",
            workspaceBoard,
        });
        await deleteWorkspaceBoard(workspaceBoard, { fetch });
    }
    // TODO create shared layout for archive and settings
</script>

<div class="flex min-h-full w-full flex-col items-center bg-background py-8">
    <main class="flex w-full max-w-xl flex-col gap-4">
        <h1 class="text-2xl font-bold">
            {$_("workspace-board-archive.title")}
        </h1>
        <div class="flex flex-col rounded-lg bg-foreground p-4 shadow-card">
            {#each archivedWorkspaceBoards as workspaceBoard}
                <div class="flex flex-col gap-2 p-2">
                    <p class="text-truncate line-clamp-1 font-bold">
                        {workspaceBoard.title}
                    </p>
                    <div class="flex flex-row items-center justify-between">
                        <!--TODO show the archival date here-->
                        <p>
                            {$_("workspace-board-archive.card.archived", {
                                values: {
                                    archived: parseISO(
                                        workspaceBoard.archived,
                                    ),
                                },
                            })}
                        </p>
                        <!-- Buttons here -->
                        <div class="flex flex-row">
                            <Button
                                style={{ kind: "secondary" }}
                                size="small"
                                color="blue"
                                label={$_(
                                    "workspace-board-archive.card.recover",
                                )}
                                action={{
                                    kind: "button",
                                    action: recoverAction.bind(
                                        null,
                                        workspaceBoard,
                                    ),
                                }}
                            />

                            <Button
                                style={{ kind: "primary" }}
                                size="small"
                                color="red"
                                label={$_(
                                    "workspace-board-archive.card.delete",
                                )}
                                action={{
                                    kind: "button",
                                    action: deleteAction.bind(
                                        null,
                                        workspaceBoard,
                                    ),
                                }}
                            />
                        </div>
                    </div>
                </div>
            {:else}
                {$_("workspace-board-archive.empty")}
            {/each}
        </div>
    </main>
</div>
