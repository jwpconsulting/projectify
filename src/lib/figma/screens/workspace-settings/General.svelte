<script lang="ts">
    import { _ } from "svelte-i18n";

    import vars from "$lib/env";
    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateWorkspace } from "$lib/repository/workspace";
    import type { EditableViewState } from "$lib/types/ui";
    import type { Workspace } from "$lib/types/workspace";
    import { uploadImage } from "$lib/utils/file";

    export let workspace: Workspace;

    const uuid = workspace.uuid;

    let { title, description, picture } = workspace;

    let state: EditableViewState = { kind: "viewing" };

    function resetForm() {
        title = workspace.title;
        description = workspace.description;
    }

    function fieldChanged() {
        state = { kind: "editing" };
    }

    let imageFile: File | undefined = undefined;
    function fileSelected(file: File, src: string) {
        state = { kind: "editing" };
        imageFile = file;
        picture = src;
    }

    async function save() {
        state = { kind: "saving" };
        if (imageFile) {
            await uploadImage(
                imageFile,
                vars.API_ENDPOINT +
                    `/workspace/workspace/${uuid}/picture-upload`
            );
        }
        workspace = await updateWorkspace(uuid, title, description);
        resetForm();
        state = { kind: "viewing" };
    }

    function cancel() {
        state = { kind: "viewing" };
        resetForm();
    }

    async function onDelete() {
        console.log("TODO implement deletion");
        await new Promise(console.error);
    }
</script>

<form
    class="flex flex-col gap-6"
    on:submit|preventDefault={save}
    name="general"
>
    <div class="flex flex-col items-center">
        <div class="relative flex h-24 w-24 w-max flex-col">
            {#if picture}
                <img
                    src={picture}
                    class="h-full"
                    alt={$_("workspace-settings.general.picture.alt")}
                />
            {:else}
                <div class="h-24 w-24">
                    {$_("workspace-settings.general.picture.no-picture")}
                </div>
            {/if}
            <div class="absolute -bottom-1/4 -right-1/4">
                <UploadAvatar
                    label={$_("workspace-settings.general.picture.label")}
                    {fileSelected}
                />
            </div>
        </div>
    </div>
    <div class="flex flex-col gap-6">
        <InputField
            bind:value={title}
            placeholder={$_(
                "workspace-settings.general.workspace-name.placeholder"
            )}
            onClick={fieldChanged}
            style={{ kind: "field", inputType: "text" }}
            name="title"
            label={$_("workspace-settings.general.workspace-name.label")}
        />
        <InputField
            bind:value={description}
            placeholder={$_(
                "workspace-settings.general.description.placeholder"
            )}
            onClick={fieldChanged}
            style={{ kind: "field", inputType: "text" }}
            name="title"
            label={$_("workspace-settings.general.description.label")}
        />
        <Button
            action={{
                kind: "submit",
                disabled: state.kind !== "editing",
            }}
            size="medium"
            style={{ kind: "primary" }}
            color="blue"
            label={$_("workspace-settings.general.save")}
        />
        <Button
            action={{
                kind: "button",
                action: cancel,
                disabled: state.kind !== "editing",
            }}
            size="medium"
            style={{ kind: "secondary" }}
            color="blue"
            label={$_("workspace-settings.general.cancel")}
        />
        <Button
            action={{ kind: "button", action: onDelete }}
            size="medium"
            style={{ kind: "secondary" }}
            color="red"
            label={$_("workspace-settings.general.delete")}
        />
    </div>
</form>
