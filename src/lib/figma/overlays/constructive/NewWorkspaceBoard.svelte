<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Workspace } from "$lib/types/workspace";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createWorkspaceBoard } from "$lib/repository/workspace";
    import { closeConstructiveOverlay } from "$lib/stores/globalUi";

    export let workspace: Workspace;

    let title: string | null = null;

    async function perform() {
        if (!title) {
            throw new Error("Not valid");
        }
        await createWorkspaceBoard(workspace, {
            title,
            description: "TODO",
            deadline: null,
        });
        closeConstructiveOverlay();
    }
</script>

<div class="flex flex-col gap-2">
    <InputField
        name="workspace-board-name"
        label={$_("new-workspace-board.workspace-board-name")}
        placeholder={$_("new-workspace-board.enter-a-workspace-board-name")}
        style={{ kind: "field", inputType: "text" }}
        bind:value={title}
    />
    <InputField
        name="deadline"
        label={$_("new-workspace-board.deadline")}
        placeholder={$_("new-workspace-board.select-date")}
        style={{ kind: "field", inputType: "text" }}
    />
</div>
<div class="flex flex-row justify-center">
    <Button
        action={{
            kind: "button",
            action: () => {
                console.error("Cancel not implemented");
            },
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board.cancel")}
    />
    <Button
        action={{ kind: "button", action: perform }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board.create-board")}
    />
</div>
