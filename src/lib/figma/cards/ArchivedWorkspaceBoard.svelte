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
