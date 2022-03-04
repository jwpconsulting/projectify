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
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { client } from "$lib/graphql/client";
    import vars from "$lib/env";
    import {
        Mutation_UpdateWorkspace,
        Query_WorkspacesSettingsGeneral,
    } from "$lib/graphql/operations";
    import ProfilePicture from "../profilePicture.svelte";
    import { uploadImage } from "$lib/utils/file";

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

    async function saveData() {
        try {
            await client.mutate({
                mutation: Mutation_UpdateWorkspace,
                variables: {
                    input: {
                        uuid: workspaceUUID,
                        title: workspace.title,
                        description: workspace.description,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    function fieldChanged() {
        isEditMode = true;
    }

    let imageFile = null;
    function onFileSelected({ detail: { src, file } }) {
        imageFile = file;
        isEditMode = true;
        workspace.picture = src;
    }

    async function onSave() {
        isSaving = true;
        await uploadImage(
            imageFile,
            vars.API_ENDPOINT +
                `/workspace/workspace/${workspaceUUID}/picture-upload`
        );
        await saveData();
        await res.refetch();
        isSaving = false;
        isEditMode = false;
    }

    async function onCancel() {
        isSaving = false;
        console.log("cancel");
    }
    async function onDelete() {
        console.log("delete");
    }
</script>

{#if workspace}
    <div
        class:pointer-events-none={isSaving}
        class="flex flex-col space-y-4 divide-y divide-base-300"
    >
        <SettingsField label="Icon image" labelVAlign="start">
            <ProfilePictureFileSelector
                url={workspace.picture}
                on:fileSelected={onFileSelected}
                let:src
            >
                <div
                    class="border border-base-300 rounded-md bg-primary-content text-primary overflow-hidden"
                >
                    <ProfilePicture
                        typogram={workspace.title}
                        emptyIcon={null}
                        url={src}
                        size={128}
                    />
                </div>
            </ProfilePictureFileSelector>
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
