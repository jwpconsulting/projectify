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

    import type { User } from "$lib/types";

    let isEditMode = false;
    let isSaving = false;

    let imageFile: File | null = null;

    function fieldChanged() {
        isEditMode = true;
    }

    let currentUser: User | null = null;
    let fullName: string | null;
    $: {
        if (!isEditMode) {
            if ($user) {
                currentUser = { ...$user };
                fullName = currentUser
                    ? currentUser.full_name
                        ? currentUser.full_name
                        : null
                    : null;
            }
        }
    }

    function onFileSelected({
        detail: { src, file },
    }: {
        detail: { src: string; file: File };
    }) {
        imageFile = file;
        isEditMode = true;
        if (currentUser) {
            currentUser.profile_picture = src;
        }
    }

    async function saveData() {
        try {
            await client.mutate({
                mutation: Mutation_UpdateProfile,
                variables: {
                    input: {
                        fullName: fullName || "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onSave() {
        isSaving = true;
        let fileUpload: Promise<null> | null = null;
        if (imageFile) {
            fileUpload = uploadImage(
                imageFile,
                vars.API_ENDPOINT + "/user/profile-picture-upload"
            );
        }
        try {
            await Promise.all([saveData(), fileUpload]);
        } finally {
            await fetchUser();
            isSaving = false;
            isEditMode = false;
        }
    }

    function onCancel() {
        isSaving = false;
        isEditMode = false;
    }
</script>

<AuthGuard>
    <SettingPage title="My Profile">
        <div class="space-y-8">
            <header
                class="mt-[-40px] flex flex-col items-center justify-center space-y-2"
            >
                <ProfilePictureFileSelector
                    url={currentUser?.profile_picture}
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

                <div class="text-xl font-bold ">
                    <input
                        class="nowrap-ellipsis input input-bordered grow rounded-md p-2 text-center text-xl font-bold"
                        placeholder={"Full name"}
                        on:input={() => fieldChanged()}
                        bind:value={fullName}
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
