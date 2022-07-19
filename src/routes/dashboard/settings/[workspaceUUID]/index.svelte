<script lang="ts">
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import ProfilePictureFileSelector from "$lib/components/profilePictureFileSelector.svelte";
    import SettingsField from "$lib/components/dashboard/settings-field.svelte";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { _ } from "svelte-i18n";
    import { client } from "$lib/graphql/client";
    import vars from "$lib/env";
    import { Mutation_UpdateWorkspace } from "$lib/graphql/operations";
    import { getWorkspace } from "$lib/repository";
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import { uploadImage } from "$lib/utils/file";
    import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
    import type { Workspace } from "$lib/types";
    import { getContext } from "svelte";
    import { loading } from "$lib/stores/dashboard";

    let workspaceUUID: string = getContext("workspaceUUID");

    let res: Workspace | null = null;
    let workspaceWSStore: WSSubscriptionStore | null;
    let workspace: Workspace | null = null;

    async function fetch() {
        if (!workspaceUUID) {
            throw new Error("Expected workspaceUUID");
        }
        res = await getWorkspace(workspaceUUID);
        $loading = false;
    }

    const refetch = debounce(() => {
        fetch();
    }, 100);

    $: {
        if (workspaceUUID) {
            $loading = true;
            fetch();

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
        if (!isEditMode && res) {
            workspace = { ...res };
        }
    }

    let isEditMode = false;
    let isSaving = false;

    async function saveData() {
        if (!workspace) {
            throw new Error("Expected workspace");
        }
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

    let imageFile: File | null = null;
    function onFileSelected({
        detail: { src, file },
    }: {
        detail: { src: string; file: File };
    }) {
        imageFile = file;
        isEditMode = true;
        if (!workspace) {
            throw new Error("Expected workspace");
        }
        workspace.picture = src;
    }

    async function onSave() {
        isSaving = true;
        if (imageFile) {
            await uploadImage(
                imageFile,
                vars.API_ENDPOINT +
                    `/workspace/workspace/${workspaceUUID}/picture-upload`
            );
        }
        await saveData();
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
                    class="overflow-hidden rounded-md border border-base-300 bg-primary-content text-primary"
                >
                    <ProfilePicture
                        typogram={workspace.title}
                        emptyIcon={null}
                        url={src ? src : null}
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
                class="btn btn-outline  btn-accent btn-sm w-full rounded-full hover:bg-accent hover:text-accent-content"
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
