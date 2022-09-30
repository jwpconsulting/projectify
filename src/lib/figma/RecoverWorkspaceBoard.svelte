<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import Button from "$lib/figma/Button.svelte";

    export let workspaceBoard: WorkspaceBoard;
    console.log("TODO do something with", workspaceBoard);
</script>

<p class="text-center text-error">
    {$_("recover-workspace-board.notice")}
</p>
<div class="flex flex-row justify-center">
    <Button
        on:click={() => {
            console.error("Cancel not implemented");
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("recover-workspace-board.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("recover-workspace-board.recover-board")}
    />
</div>
