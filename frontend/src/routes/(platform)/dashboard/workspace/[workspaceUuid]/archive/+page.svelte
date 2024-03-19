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
        archiveProject,
        deleteProject,
    } from "$lib/repository/workspace/project";
    import { currentArchivedProjects } from "$lib/stores/dashboard";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { Project } from "$lib/types/workspace";

    $: archivedProjects = $currentArchivedProjects ?? [];

    async function recoverAction(project: Project) {
        await openConstructiveOverlay({
            kind: "recoverProject",
            project,
        });
        await archiveProject(project, false, { fetch });
    }

    async function deleteAction(project: Project) {
        await openDestructiveOverlay({
            kind: "deleteProject",
            project,
        });
        await deleteProject(project, { fetch });
    }
</script>

<main class="flex w-full max-w-xl flex-col gap-4">
    <h1 class="text-2xl font-bold">
        {$_("project-archive.title")}
    </h1>
    <div class="flex flex-col rounded-lg bg-foreground p-4 shadow-card">
        {#each archivedProjects as project}
            <div class="flex flex-col gap-2 p-2">
                <p class="font-bold">
                    {project.title}
                </p>
                <div class="flex flex-row items-center justify-between">
                    <!--TODO show the archival date here-->
                    <p>
                        {$_("project-archive.card.archived", {
                            values: {
                                archived: parseISO(project.archived),
                            },
                        })}
                    </p>
                    <!-- Buttons here -->
                    <div class="flex flex-row">
                        <Button
                            style={{ kind: "secondary" }}
                            size="medium"
                            color="blue"
                            label={$_("project-archive.card.recover")}
                            action={{
                                kind: "button",
                                action: recoverAction.bind(null, project),
                            }}
                        />

                        <Button
                            style={{ kind: "primary" }}
                            size="medium"
                            color="red"
                            label={$_("project-archive.card.delete")}
                            action={{
                                kind: "button",
                                action: deleteAction.bind(null, project),
                            }}
                        />
                    </div>
                </div>
            </div>
        {:else}
            {$_("project-archive.empty")}
        {/each}
    </div>
</main>
