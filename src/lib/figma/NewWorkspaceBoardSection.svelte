<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types";
    import Button from "$lib/figma/Button.svelte";
    import InputField from "$lib/figma/InputField.svelte";

    export let workspaceBoard: WorkspaceBoard;
    console.log("TODO do something with", workspaceBoard);
</script>

<div class="flex flex-col gap-2">
    <InputField
        name="workspace-board-name"
        label={$_("new-workspace-board-section.new-section-name-label")}
        placeholder={$_("new-workspace-board-section.new-section-name")}
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
        label={$_("new-workspace-board-section.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board-section.create-section")}
    />
</div>
