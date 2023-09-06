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
    <svelte:fragment slot="form">
        <p class="text-center text-error">
            {$_("overlay.constructive.recover-workspace-board.notice")}
        </p>
        <div class="flex flex-row justify-center">
            <Button
                action={{
                    kind: "button",
                    action: rejectConstructiveOverlay,
                }}
                style={{ kind: "secondary" }}
                size="medium"
                color="blue"
                label={$_(
                    "overlay.constructive.recover-workspace-board.cancel"
                )}
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
                label={$_(
                    "overlay.constructive.recover-workspace-board.recover-board"
                )}
            />
        </div>
    </svelte:fragment>
</Layout>
