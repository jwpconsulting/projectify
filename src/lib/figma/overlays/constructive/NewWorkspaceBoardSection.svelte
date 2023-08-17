<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createWorkspaceBoardSection } from "$lib/repository/workspace";
    import type {
        CreateWorkspaceBoardSection,
        WorkspaceBoard,
    } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;
    export let close: () => void;

    let title: string;

    function cancel() {
        close();
    }

    async function perform() {
        const workspaceBoardSection: CreateWorkspaceBoardSection = {
            title: title,
            description: "",
        };
        await createWorkspaceBoardSection(
            workspaceBoard,
            workspaceBoardSection
        );
        close();
    }
</script>

<div class="flex flex-col gap-2">
    <InputField
        name="workspace-board-name"
        label={$_("new-workspace-board-section.new-section-name-label")}
        placeholder={$_("new-workspace-board-section.new-section-name")}
        style={{ kind: "field", inputType: "text" }}
        bind:value={title}
    />
</div>
<div class="flex flex-row justify-center">
    <Button
        action={{ kind: "button", action: cancel }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board-section.cancel")}
    />
    <Button
        action={{ kind: "button", action: perform }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board-section.create-section")}
    />
</div>
