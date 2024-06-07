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

    import Loading from "$lib/components/Loading.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { currentProject } from "$lib/stores/dashboard/project";
    import { getDashboardProjectUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    export let data: PageData;
    $: project = $currentProject;
    $: backUrl = project ? getDashboardProjectUrl(project) : undefined;
</script>

{#await data.tasks}
    <Loading />
{:then tasks}
    {#if tasks.length}
        <div class="flex flex-col gap-6 bg-foreground px-4 pb-6 pt-4">
            <div class="flex flex-col gap-2">
                <h1 class="text-xl font-bold">
                    {$_("dashboard.search.found.title", {
                        values: { search: data.search },
                    })}
                </h1>
                {#if backUrl}
                    <p>
                        <Anchor
                            label={$_("dashboard.search.found.back")}
                            size="normal"
                            href={backUrl}
                        />
                    </p>
                {/if}
            </div>
            <div class="flex flex-col gap-1">
                {#if project}
                    {#each tasks as task}
                        <TaskCard {task} {project} />
                    {/each}
                {/if}
            </div>
            {#if backUrl}
                <p>
                    <Anchor
                        label={$_("dashboard.search.found.back")}
                        size="normal"
                        href={backUrl}
                    />
                </p>
            {/if}
        </div>
    {:else if backUrl}
        <div class="flex items-center justify-center py-6">
            <div
                class="flex flex-col gap-4 rounded-md bg-base-100 p-6 shadow-sm"
            >
                <p class="font-bold">
                    {$_("dashboard.search.not-found.title", {
                        values: { search: data.search },
                    })}
                </p>
                <p class="max-w-md">
                    {$_("dashboard.search.not-found.explanation")}
                </p>
                <p>
                    <Anchor
                        label={$_("dashboard.search.not-found.back")}
                        size="normal"
                        href={backUrl}
                    />
                </p>
            </div>
        </div>
    {/if}
{/await}
