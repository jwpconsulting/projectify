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
    import { _ } from "svelte-i18n";

    import ArchivedWorkspaceBoard from "$lib/figma/cards/ArchivedWorkspaceBoard.svelte";
    import { currentArchivedWorkspaceBoards } from "$lib/stores/dashboard";

    $: archivedWorkspaceBoards = $currentArchivedWorkspaceBoards ?? [];
</script>

<div class="flex min-h-full w-full flex-col items-center bg-background py-8">
    <main class="flex w-full max-w-xl flex-col gap-4">
        <h1 class="text-2xl font-bold">
            {$_("workspace-board-archive.title")}
        </h1>
        <div class="flex flex-col rounded-lg bg-foreground p-4 shadow-card">
            {#each archivedWorkspaceBoards as workspaceBoard}
                <ArchivedWorkspaceBoard {workspaceBoard} />
            {:else}
                {$_("workspace-board-archive.empty")}
            {/each}
        </div>
    </main>
</div>
