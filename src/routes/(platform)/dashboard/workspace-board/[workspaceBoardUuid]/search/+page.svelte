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

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    $: workspaceBoard = data.workspaceBoard;
    $: tasks = data.tasks;
    $: search = data.search;
</script>

{#if tasks.length}
    <div class="px-4 py-6">
        <p class="text-xl font-bold">
            {$_("dashboard.showing-results-for-search", {
                values: { search },
            })}
        </p>
    </div>
    <div class="flex flex-col p-2">
        {#each tasks as task}
            <TaskCard {task} {workspaceBoard} />
        {/each}
    </div>
{:else}
    <div class="flex items-center justify-center py-6">
        <div class="rounded-md bg-base-100 p-6 font-bold shadow-sm">
            {$_("dashboard.tasks-not-found-for", {
                values: { search },
            })}
        </div>
    </div>
{/if}
