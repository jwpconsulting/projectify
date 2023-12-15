<script lang="ts">
    import WorkspaceBoardSections from "$lib/components/dashboard/WorkspaceBoardSections.svelte";
    import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoardDetail } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoardDetail;

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        });
    }
</script>

<!-- Sections -->
<div class="flex flex-col gap-4 p-2">
    <WorkspaceBoardSections {workspaceBoard} />
</div>
<div class="self-end p-2">
    <FloatingActionButton icon="plus" action={onAddNewSection} />
</div>
