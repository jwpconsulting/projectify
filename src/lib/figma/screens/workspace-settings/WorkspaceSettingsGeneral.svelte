<script lang="ts">
    import { _ } from "svelte-i18n";

    import WorkspaceSettingsPage from "$lib/figma/screens/workspace-settings/WorkspaceSettingsPage.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;

    let title: string = workspace.title;
    let description: string | undefined = workspace.description;
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
            action={{ kind: "button", action: console.error }}
            size="medium"
            style={{ kind: "primary" }}
            color="red"
            label={$_("settings.delete-workspace")}
        />
    </form>
</WorkspaceSettingsPage>
