<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createWorkspaceBoardSection } from "$lib/repository/workspace/workspaceBoardSection";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type {
        CreateWorkspaceBoardSection,
        WorkspaceBoard,
    } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    let title: string;

    async function onSubmit() {
        const workspaceBoardSection: CreateWorkspaceBoardSection = {
            title: title,
            description: "",
        };
        await createWorkspaceBoardSection(
            workspaceBoard,
            workspaceBoardSection,
            { fetch },
        );
        resolveConstructiveOverlay();
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.create-workspace-board-section.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.create-workspace-board-section.form.title.label",
            )}
            placeholder={$_(
                "overlay.constructive.create-workspace-board-section.form.title.placeholder",
            )}
            style={{ inputType: "text" }}
            bind:value={title}
        />
    </svelte:fragment>
    <svelte:fragment slot="buttons">
        <Button
            action={{ kind: "button", action: rejectConstructiveOverlay }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.create-workspace-board-section.cancel",
            )}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.create-workspace-board-section.create-section",
            )}
        />
    </svelte:fragment>
</Layout>
