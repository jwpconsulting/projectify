<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;
    console.log("TODO do something with", workspaceBoard);
</script>

<Layout>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.recover-workspace-board.title")}
    </svelte:fragment>
    <svelte:fragment slot="message">
        <p class="text-center text-error">
            {$_("overlay.constructive.recover-workspace-board.notice")}
        </p>
    </svelte:fragment>
    <svelte:fragment slot="buttons">
        <Button
            action={{
                kind: "button",
                action: rejectConstructiveOverlay,
            }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.recover-workspace-board.cancel")}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.recover-workspace-board.recover-board"
            )}
        />
    </svelte:fragment>
</Layout>
