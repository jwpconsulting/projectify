<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectDestructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;
    console.log("TODO do something with", workspaceBoard);
</script>

<p class="text-center text-error">
    {$_("recover-workspace-board.notice")}
</p>
<div class="flex flex-row justify-center">
    <Button
        action={{
            kind: "button",
            action: rejectDestructiveOverlay,
        }}
        style={{ kind: "secondary" }}
        size="medium"
        color="blue"
        label={$_("recover-workspace-board.cancel")}
    />
    <Button
        action={{
            kind: "button",
            action: () => {
                console.error("Save not implemented");
            },
        }}
        style={{ kind: "primary" }}
        size="medium"
        color="blue"
        label={$_("recover-workspace-board.recover-board")}
    />
</div>
