<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import ProfilePictureFileSelector from "$lib/components/profilePictureFileSelector.svelte";
    import { fetchUser, user } from "$lib/stores/user";
    import { _ } from "svelte-i18n";

    import vars from "$lib/env";
    import { client } from "$lib/graphql/client";
    import { Mutation_UpdateProfile } from "$lib/graphql/operations";
    import { uploadImage } from "$lib/utils/file";
    import UserProfilePicture from "$lib/components/userProfilePicture.svelte";

    let isEditMode = false;
    let isSaving = false;

    let imageFile = null;

    function fieldChanged() {
        isEditMode = true;
    }

    let currentUser = null;
    $: {
        if (!isEditMode) {
            currentUser = { ...$user };
        }
    }

    function onFileSelected({ detail: { src, file } }) {
        imageFile = file;
        isEditMode = true;
        currentUser.profilePicture = src;
    }

    let uploadRequest = null;

    async function saveData() {
        try {
            await client.mutate({
                mutation: Mutation_UpdateProfile,
                variables: {
                    input: {
                        fullName: currentUser.fullName || "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onSave() {
        isSaving = true;
        await uploadImage(
            imageFile,
            vars.API_ENDPOINT + "/user/profile-picture-upload"
        );
        await saveData();
        await fetchUser();
        isSaving = false;
        isEditMode = false;
    }

    async function onCancel() {
        if (uploadRequest) {
            isSaving = false;
            uploadRequest.abort();
        }
    }
</script>

<AuthGuard>
    <SettingPage title="My Profile">
        <div class="space-y-8">
            <header
                class="flex flex-col justify-center items-center space-y-2 mt-[-40px]"
            >
                <ProfilePictureFileSelector
                    url={currentUser ? currentUser.profilePicture : null}
                    on:fileSelected={onFileSelected}
                    let:src
                >
                    <UserProfilePicture
                        pictureProps={{
                            url: src,
                            size: 128,
                        }}
                    />
                </ProfilePictureFileSelector>

                <div class="font-bold text-xl ">
                    <input
                        class="grow text-xl text-center p-2 rounded-md nowrap-ellipsis font-bold"
                        placeholder={"Full name"}
                        on:input={() => fieldChanged()}
                        bind:value={currentUser.fullName}
                    />
                </div>
            </header>

            <SettingFooterEditSaveButtons
                {isSaving}
                bind:isEditMode
                on:save={onSave}
                on:cancel={onCancel}
            />
        </div>
    </SettingPage>
</AuthGuard>
