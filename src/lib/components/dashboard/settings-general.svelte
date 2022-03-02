<script lang="ts">
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import { _ } from "svelte-i18n";
    import UserProfilePictureFileSelector from "../userProfilePictureFileSelector.svelte";
    import SettingsField from "./settings-field.svelte";
    let isEditMode = false;
    let isSaving = false;

    async function onSave() {
        console.log("save");
    }
    async function onCancel() {
        console.log("cancel");
    }
    async function onDelete() {
        console.log("delete");
    }

    let fileds = [];
</script>

<div class="flex flex-col space-y-4 divide-y divide-base-300">
    <SettingsField label="Icon image" labelVAlign="start">
        <UserProfilePictureFileSelector />
    </SettingsField>
    <SettingsField label="Project Name">
        <input
            type="email"
            id="email"
            name="email"
            autocomplete="email"
            placeholder={"place g"}
            class="input input-bordered w-full"
        />
    </SettingsField>
    <SettingsField label="Description">
        <textarea rows="5" class="textarea textarea-bordered w-full"
            >{"text"}</textarea
        >
    </SettingsField>
    <SettingsField label="Danger Zone">
        <button
            class:loading={isSaving}
            class="btn btn-accent  w-full btn-outline btn-sm rounded-full hover:bg-accent hover:text-accent-content"
            on:click={onDelete}
        >
            {"Delete Workspace"}
        </button>
    </SettingsField>
</div>

<SettingFooterEditSaveButtons
    {isSaving}
    bind:isEditMode
    on:save={onSave}
    on:cancel={onCancel}
/>
