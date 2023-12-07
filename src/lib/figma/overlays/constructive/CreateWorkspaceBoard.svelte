<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { createWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    export let workspace: Workspace;

    let title: string | undefined = undefined;

    async function onSubmit() {
        if (!title) {
            throw new Error("Not valid");
        }
        const { uuid } = await createWorkspaceBoard(
            workspace,
            {
                title,
                description: "TODO",
            },
            { fetch }
        );
        await goto(getDashboardWorkspaceBoardUrl(uuid));
        resolveConstructiveOverlay();
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.create-workspace-board.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.create-workspace-board.form.title.label"
            )}
            placeholder={$_(
                "overlay.constructive.create-workspace-board.form.title.placeholder"
            )}
            style={{ inputType: "text" }}
            bind:value={title}
        />
        <InputField
            name="deadline"
            label={$_(
                "overlay.constructive.create-workspace-board.form.deadline.label"
            )}
            placeholder={$_(
                "overlay.constructive.create-workspace-board.form.deadline.placeholder"
            )}
            style={{ inputType: "text" }}
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
            label={$_("overlay.constructive.create-workspace-board.cancel")}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.create-workspace-board.create-board"
            )}
        />
    </svelte:fragment>
</Layout>
