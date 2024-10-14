<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import parseISO from "date-fns/parseISO";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentArchivedProjects } from "$lib/stores/dashboard/archive";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { ArchivedProject } from "$lib/types/workspace";
    import { openApiClient } from "$lib/repository/util";

    $: archivedProjects = $currentArchivedProjects ?? [];

    async function recoverAction(project: ArchivedProject) {
        await openConstructiveOverlay({
            kind: "recoverProject",
            project,
        });
    }

    async function deleteAction(project: ArchivedProject) {
        await openDestructiveOverlay({
            kind: "deleteProject",
            project,
        });
        await openApiClient.DELETE("/workspace/project/{project_uuid}", {
            params: { path: { project_uuid: project.uuid } },
        });
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
                    <p>
                        {$_("project-archive.card.archived", {
                            values: {
                                archived:
                                    project.archived &&
                                    parseISO(project.archived),
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
