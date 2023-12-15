<script lang="ts">
    import { _ } from "svelte-i18n";

    import WorkspaceBoardSectionC from "$lib/figma/cards/WorkspaceBoardSection.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentWorkspaceBoardSections } from "$lib/stores/dashboard";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type {
        WorkspaceBoardSectionWithTasks,
        WorkspaceBoardDetail,
    } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoardDetail;

    let workspaceBoardSections: WorkspaceBoardSectionWithTasks[];
    $: workspaceBoardSections =
        $currentWorkspaceBoardSections ??
        workspaceBoard.workspace_board_sections;

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        });
    }
</script>

{#each workspaceBoardSections as workspaceBoardSection (workspaceBoardSection.uuid)}
    <WorkspaceBoardSectionC {workspaceBoard} {workspaceBoardSection} />
{:else}
    <section class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col">
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
