<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types";
    import Button from "$lib/figma/Button.svelte";
    import InputField from "$lib/figma/InputField.svelte";

    // TODO do something with workspaceBoard
    export let workspaceBoard: WorkspaceBoard;
    console.log(workspaceBoard);
</script>

<div class="flex flex-col gap-2">
    <div class="flex flex-col">
        <label for="workspace-board-name"
            >{$_("edit-workspace-board.please-edit-me")}</label
        >
        <InputField
            name="workspace-board-name"
            placeholder={$_("edit-workspace-board.please-edit-me")}
            style="field"
        />
    </div>
    <div class="">
        <label for="deadline"
            >{$_("edit-workspace-board.please-edit-me")}</label
        >
        <InputField
            name="deadline"
            placeholder={$_("edit-workspace-board.please-edit-me")}
            style="field"
        />
    </div>
</div>
<div class="flex flex-row">
    <Button
        on:click={() => {
            console.error("Cancel not implemented");
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
    >
        {$_("edit-workspace-board.cancel")}
    </Button>
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
    >
        {$_("edit-workspace-board.save")}
    </Button>
</div>
