<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    let title = workspaceBoard.title;
    let deadline = workspaceBoard.deadline;

    async function onSubmit() {
        const updatedWorkspaceBoard = {
            ...workspaceBoard,
            title,
            deadline,
        };
        await updateWorkspaceBoard(updatedWorkspaceBoard, { fetch });
        resolveConstructiveOverlay();
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.update-workspace-board.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            label={$_(
                "overlay.constructive.update-workspace-board.form.title.label"
            )}
            name="workspace-board-name"
            placeholder={$_(
                "overlay.constructive.update-workspace-board.form.title.placeholder"
            )}
            style={{ kind: "field", inputType: "text" }}
            bind:value={title}
            required
        />
        <InputField
            name="deadline"
            label={$_(
                "overlay.constructive.update-workspace-board.form.deadline.label"
            )}
            placeholder={$_(
                "overlay.constructive.update-workspace-board.form.deadline.placeholder"
            )}
            style={{ kind: "field", inputType: "date" }}
            bind:value={deadline}
        />
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
            label={$_("overlay.constructive.update-workspace-board.cancel")}
        />
        <Button
            action={{
                kind: "submit",
            }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.update-workspace-board.save")}
        />
    </svelte:fragment>
</Layout>
