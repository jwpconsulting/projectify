<script lang="ts">
    import { _ } from "svelte-i18n";

    import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";
    import SectionBar from "$lib/figma/cards/SectionBar.svelte";
    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        createCurrentSearchedTasks,
        currentWorkspaceBoardSections,
        taskSearchInput,
    } from "$lib/stores/dashboard";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    const currentSearchedTasks = createCurrentSearchedTasks(
        currentWorkspaceBoardSections,
        taskSearchInput
    );

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        });
    }
</script>

<!-- XXX: setting overflow-x-auto here magically solves an overflowing task card
    Why? Justus 2023-08-28 -->
<div class="flex min-h-full flex-auto flex-col overflow-x-auto bg-base-200">
    {#if $currentSearchedTasks}
        <!-- Flat Tasks Results -->
        {#if $currentSearchedTasks.length}
            <div class="flex flex-col p-2">
                {#each $currentSearchedTasks as task}
                    <TaskCard {task} />
                {/each}
            </div>
        {:else}
            <div class="flex items-center justify-center">
                <div class="rounded-md bg-base-100 p-6 shadow-sm">
                    {$_("tasks-not-found-for")} "{$taskSearchInput}"
                </div>
            </div>
        {/if}
    {:else}
        <!-- Sections -->
        <div class="flex flex-col gap-16 p-2">
            {#each $currentWorkspaceBoardSections as workspaceBoardSection (workspaceBoardSection.uuid)}
                <SectionBar {workspaceBoard} {workspaceBoardSection} />
            {:else}
                <section
                    class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col"
                >
                    <p>
                        {$_("dashboard.no-sections.message")}
                    </p>
                    <Button
                        style={{ kind: "primary" }}
                        color="blue"
                        size="small"
                        grow={false}
                        label={$_("dashboard.no-sections.prompt")}
                        action={{ kind: "button", action: onAddNewSection }}
                    />
                </section>
            {/each}
        </div>
    {/if}
    <div class="absolute bottom-4 right-4">
        <FloatingActionButton icon="plus" action={onAddNewSection} />
    </div>
</div>
