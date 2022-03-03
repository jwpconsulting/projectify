<script lang="ts">
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import { _ } from "svelte-i18n";
    import ProfilePictureFileSelector from "../profilePictureFileSelector.svelte";
    import SettingsField from "./settings-field.svelte";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import Loading from "../loading.svelte";
    import ProfilePicture from "../profilePicture.svelte";
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { client } from "$lib/graphql/client";
    import { Query_WorkspacesSettingsGeneral } from "$lib/graphql/operations";

    export let workspaceUUID = null;
    let res = null;
    let workspaceWSStore;
    let workspace = null;

    const refetch = debounce(() => {
        res.refetch();
    }, 100);

    $: {
        if (workspaceUUID) {
            res = query(Query_WorkspacesSettingsGeneral, {
                variables: { uuid: workspaceUUID },
                fetchPolicy: "network-only",
            });

            workspaceWSStore = getSubscriptionForCollection(
                "workspace",
                workspaceUUID
            );
        }
    }

    $: {
        if ($workspaceWSStore) {
            refetch();
        }
    }

    $: {
        if (!isEditMode && res && $res.data) {
            workspace = { ...$res.data["workspace"] };
        }
    }

    let isEditMode = false;
    let isSaving = false;

    async function onSave() {
        isSaving = true;
        console.log("save");
    }
    async function onCancel() {
        isSaving = false;
        console.log("cancel");
    }
    async function onDelete() {
        console.log("delete");
    }

    function fieldChanged() {
        isEditMode = true;
    }
</script>

{#if workspace}
    <div
        class:pointer-events-none={isSaving}
        class="flex flex-col space-y-4 divide-y divide-base-300"
    >
        <SettingsField label="Icon image" labelVAlign="start">
            <ProfilePictureFileSelector />
        </SettingsField>
        <SettingsField label="Project Name">
            <input
                type="text"
                id="title"
                name="title"
                autocomplete="email"
                placeholder={"Workspace title"}
                class="input input-bordered w-full"
                on:input={fieldChanged}
                bind:value={workspace.title}
            />
        </SettingsField>
        <SettingsField label="Description">
            <textarea
                rows="5"
                class="textarea textarea-bordered w-full"
                on:input={fieldChanged}>{workspace.description}</textarea
            >
        </SettingsField>
        <SettingsField label="Danger Zone">
            <button
                disabled={isSaving}
                class="btn btn-accent  w-full btn-outline btn-sm rounded-full hover:bg-accent hover:text-accent-content"
                on:click={onDelete}
            >
                {"Delete Workspace"}
            </button>
        </SettingsField>
    </div>
{/if}

<SettingFooterEditSaveButtons
    {isSaving}
    bind:isEditMode
    on:save={onSave}
    on:cancel={onCancel}
/>
