<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createWorkspaceBoardSection } from "$lib/repository/workspace";
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

    async function save() {
        const workspaceBoardSection: CreateWorkspaceBoardSection = {
            title: title,
            description: "",
        };
        await createWorkspaceBoardSection(
            workspaceBoard,
            workspaceBoardSection
        );
        resolveConstructiveOverlay();
    }
</script>

<form class="flex flex-col gap-8" on:submit|preventDefault={save}>
    <input type="submit" class="hidden" />
    <div class="flex flex-col gap-2">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.create-workspace-board-section.form.title.label"
            )}
            placeholder={$_(
                "overlay.constructive.create-workspace-board-section.form.title.placeholder"
            )}
            style={{ kind: "field", inputType: "text" }}
            bind:value={title}
        />
    </div>
    <div class="flex flex-row justify-center">
        <Button
            action={{ kind: "button", action: rejectConstructiveOverlay }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.create-workspace-board-section.cancel"
            )}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.create-workspace-board-section.create-section"
            )}
        />
    </div>
</form>
