<script lang="ts">
    import { _ } from "svelte-i18n";
    $_("");
    import WorkspaceSettingsPage from "$lib/figma/WorkspaceSettingsPage.svelte";
    import InputField from "$lib/figma/InputField.svelte";
    import Button from "$lib/figma/Button.svelte";
    import type { Workspace } from "$lib/types";
    export let workspace: Workspace;

    let title: string;
    let description: string;

    function reset() {
        title = workspace.title;
        description = workspace.description || "";
    }

    $: {
        if (workspace) {
            reset();
        }
    }
</script>

<WorkspaceSettingsPage {workspace} activeSetting="index">
    <form class="flex flex-col gap-6">
        <InputField
            bind:value={title}
            placeholder={$_("settings.enter-a-workspace-name")}
            style={{ kind: "field", inputType: "text" }}
            name="title"
            label={$_("settings.workspace-name")}
        />
        <InputField
            bind:value={description}
            placeholder={$_("settings.enter-a-description")}
            style={{ kind: "field", inputType: "text" }}
            name="title"
            label={$_("settings.enter-a-description")}
        />
        <Button
            size="medium"
            style={{ kind: "primary" }}
            color="red"
            label={$_("settings.delete-workspace")}
            disabled={false}
        />
    </form>
</WorkspaceSettingsPage>
