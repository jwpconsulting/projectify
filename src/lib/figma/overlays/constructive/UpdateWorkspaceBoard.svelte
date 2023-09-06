<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateWorkspaceBoard } from "$lib/repository/workspace";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    let title = workspaceBoard.title;
    let deadline = workspaceBoard.deadline;

    async function save() {
        const updatedWorkspaceBoard = {
            ...workspaceBoard,
            title,
            deadline,
        };
        await updateWorkspaceBoard(updatedWorkspaceBoard);
        resolveConstructiveOverlay();
    }
</script>

<form on:submit|preventDefault={save}>
    <input type="submit" class="hidden" />
    <div class="flex flex-col gap-2">
        <InputField
            label={$_(
                "overlay.constructive.edit-workspace-board.workspace-board-name"
            )}
            name="workspace-board-name"
            placeholder={$_(
                "overlay.constructive.edit-workspace-board.enter-a-workspace-board-name"
            )}
            style={{ kind: "field", inputType: "text" }}
            bind:value={title}
        />
        <InputField
            name="deadline"
            label={$_("overlay.constructive.edit-workspace-board.deadline")}
            placeholder={$_(
                "overlay.constructive.edit-workspace-board.deadline"
            )}
            style={{ kind: "field", inputType: "date" }}
            bind:value={deadline}
        />
    </div>
    <div class="flex flex-row justify-center">
        <Button
            action={{
                kind: "button",
                action: rejectConstructiveOverlay,
            }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.edit-workspace-board.cancel")}
        />
        <Button
            action={{
                kind: "submit",
            }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.edit-workspace-board.save")}
        />
    </div>
</form>
