<script lang="ts">
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import { _ } from "svelte-i18n";
    let isEditMode = false;
    let isSaving = false;

    async function onSave() {
        console.log("save");
    }
    async function onCancel() {
        console.log("cancel");
    }
</script>

<div class="flex justify-start">
    <button
        class:loading={isSaving}
        class="btn btn-accent btn-ghost text-accent btn-sm rounded-full hover:bg-accent hover:text-accent-content"
        on:click={() => {}}
    >
        {"Delete Workspace"}
    </button>
</div>

<SettingFooterEditSaveButtons
    {isSaving}
    bind:isEditMode
    on:save={onSave}
    on:cancel={onCancel}
/>
