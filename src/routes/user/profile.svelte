<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import UserProfilePictureFileSelector from "$lib/components/userProfilePictureFileSelector.svelte";
    import { fetchUser, user } from "$lib/stores/user";
    import { _ } from "svelte-i18n";

    import vars from "$lib/env";
    import { client } from "$lib/graphql/client";
    import { Mutation_UpdateProfile } from "$lib/graphql/operations";

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

    function onFileSelected({ detail: { file } }) {
        imageFile = file;
        isEditMode = true;
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === name + "=") {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1)
                    );
                    break;
                }
            }
        }
        return cookieValue;
    }

    let uploadRequest = null;

    async function uploadImage() {
        if (!imageFile) {
            return new Promise((resolve) => {
                resolve(null);
            });
        }

        if (uploadRequest) {
            uploadRequest.abort();
        }

        const formData = new FormData();
        formData.append("file", imageFile);
        uploadRequest = new XMLHttpRequest();
        uploadRequest.withCredentials = true;
        uploadRequest.open(
            "POST",
            vars.API_ENDPOINT + "/user/profile-picture-upload"
        );

        const csrftoken = getCookie("csrftoken");
        uploadRequest.setRequestHeader("X-CSRFToken", csrftoken);

        uploadRequest.send(formData);

        const promise = new Promise((resolve, reject) => {
            uploadRequest.onload = () => {
                if (
                    uploadRequest.status === 200 ||
                    uploadRequest.status === 204
                ) {
                    resolve(uploadRequest.response);
                } else {
                    reject(Error(uploadRequest.statusText));
                }
            };
        });
        return promise;
    }

    async function saveData() {
        try {
            await client.mutate({
                mutation: Mutation_UpdateProfile,
                variables: {
                    input: {
                        fullName: currentUser.fullName,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onSave() {
        isSaving = true;
        await uploadImage();
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
                <UserProfilePictureFileSelector
                    user={currentUser}
                    on:fileSelected={onFileSelected}
                />

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
