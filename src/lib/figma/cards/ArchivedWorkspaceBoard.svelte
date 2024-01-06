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
    import parseISO from "date-fns/parseISO";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        archiveWorkspaceBoard,
        deleteWorkspaceBoard,
    } from "$lib/repository/workspace/workspaceBoard";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { ArchivedWorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: ArchivedWorkspaceBoard;
    $: archived = parseISO(workspaceBoard.archived);

    async function recoverAction() {
        await openConstructiveOverlay({
            kind: "recoverWorkspaceBoard",
            workspaceBoard,
        });
        await archiveWorkspaceBoard(workspaceBoard, false, { fetch });
    }

    async function deleteAction() {
        await openDestructiveOverlay({
            kind: "deleteWorkspaceBoard",
            workspaceBoard,
        });
        await deleteWorkspaceBoard(workspaceBoard, { fetch });
    }
</script>

<div class="flex flex-col gap-2 p-2">
    <p class="text-truncate line-clamp-1 font-bold">{workspaceBoard.title}</p>
    <div class="flex flex-row items-center justify-between">
        <!--TODO show the archival date here-->
        <p>
            {$_("workspace-board-archive.card.archived", {
                values: { archived },
            })}
        </p>
        <!-- Buttons here -->
        <div class="flex flex-row">
            <Button
                style={{ kind: "secondary" }}
                size="small"
                color="blue"
                label={$_("workspace-board-archive.card.recover")}
                action={{ kind: "button", action: recoverAction }}
            />

            <Button
                style={{ kind: "primary" }}
                size="small"
                color="red"
                label={$_("workspace-board-archive.card.delete")}
                action={{ kind: "button", action: deleteAction }}
            />
        </div>
    </div>
</div>
