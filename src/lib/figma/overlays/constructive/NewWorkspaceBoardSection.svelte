<script lang="ts">
    import { _ } from "svelte-i18n";
    import type {
        WorkspaceBoard,
        CreateWorkspaceBoardSection,
    } from "$lib/types/workspace";
    import type { NewWorkspaceBoardSectionModule } from "$lib/types/stores";
    import Button from "$lib/figma/buttons/Button.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";

    export let workspaceBoard: WorkspaceBoard;
    export let close: () => void;

    export let newWorkspaceBoardSectionModule: NewWorkspaceBoardSectionModule;

    let title: string;

    let { createWorkspaceBoardSection } = newWorkspaceBoardSectionModule;

    function cancel() {
        close();
    }

    function perform() {
        const workspaceBoardSection: CreateWorkspaceBoardSection = {
            title: title,
            description: "",
        };
        createWorkspaceBoardSection(workspaceBoard, workspaceBoardSection);
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
        on:click={cancel}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board-section.cancel")}
    />
    <Button
        on:click={perform}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace-board-section.create-section")}
    />
</div>
