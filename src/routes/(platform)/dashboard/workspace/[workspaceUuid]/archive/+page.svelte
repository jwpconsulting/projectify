<script lang="ts">
    import { _ } from "svelte-i18n";

    import ArchiveWorkspaceBoard from "$lib/figma/cards/ArchiveWorkspaceBoard.svelte";
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
                <ArchiveWorkspaceBoard {workspaceBoard} />
            {:else}
                {$_("workspace-board-archive.empty")}
            {/each}
        </div>
    </main>
</div>
