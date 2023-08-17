<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateWorkspaceBoard } from "$lib/repository/workspace";
    import { closeConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    // TODO do something with workspaceBoard
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
        closeConstructiveOverlay();
    }
</script>

<div class="flex flex-col gap-2">
    <InputField
        label={$_("edit-workspace-board.workspace-board-name")}
        name="workspace-board-name"
        placeholder={$_("edit-workspace-board.enter-a-workspace-board-name")}
        style={{ kind: "field", inputType: "text" }}
        bind:value={title}
    />
    <InputField
        name="deadline"
        label={$_("edit-workspace-board.deadline")}
        placeholder={$_("edit-workspace-board.deadline")}
        style={{ kind: "field", inputType: "date" }}
        bind:value={deadline}
    />
</div>
<div class="flex flex-row justify-center">
    <Button
        action={{
            kind: "button",
            action: closeConstructiveOverlay,
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("edit-workspace-board.cancel")}
    />
    <Button
        action={{
            kind: "button",
            action: save,
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("edit-workspace-board.save")}
    />
</div>
