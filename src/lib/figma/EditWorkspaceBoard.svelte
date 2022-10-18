<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import Button from "$lib/figma/buttons/Button.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";

    // TODO do something with workspaceBoard
    export let workspaceBoard: WorkspaceBoard;
    console.log(workspaceBoard);
</script>

<div class="flex flex-col gap-2">
    <InputField
        label={$_("edit-workspace-board.workspace-board-name")}
        name="workspace-board-name"
        placeholder={$_("edit-workspace-board.enter-a-workspace-board-name")}
        style={{ kind: "field", inputType: "text" }}
    />
    <InputField
        name="deadline"
        label={$_("edit-workspace-board.deadline")}
        placeholder={$_("edit-workspace-board.deadline")}
        style={{ kind: "field", inputType: "text" }}
    />
</div>
<div class="flex flex-row justify-center">
    <Button
        on:click={() => {
            console.error("Cancel not implemented");
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("edit-workspace-board.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("edit-workspace-board.save")}
    />
</div>
