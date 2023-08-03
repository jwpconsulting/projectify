<script lang="ts">
    import { _ } from "svelte-i18n";
    import SettingFooterEditSaveButtons from "$lib/components/settingFooterEditSaveButtons.svelte";
    import SettingsPage from "$lib/components/SettingsPage.svelte";
    import ProfilePictureFileSelector from "$lib/components/profilePictureFileSelector.svelte";
    import { fetchUser, updateUserProfile } from "$lib/stores/user";

    import UserProfilePicture from "$lib/components/userProfilePicture.svelte";
    import type { PageData } from "./$types";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { unwrap } from "$lib/utils/type";
    import { updateProfilePicture } from "$lib/repository/user";

    export let data: PageData;

    let state: "viewing" | "editing" | "saving" = "viewing";

    let imageFile: File | null = null;

    let { user: currentUser } = data;
    let fullName: string | undefined;

    function onFileSelected({
        detail: { src, file },
    }: {
        detail: { src: string; file: File };
    }) {
        imageFile = file;
        state = "editing";
        if (currentUser) {
            currentUser.profile_picture = src;
        }
    }

    async function saveData() {
        if (!fullName) {
            throw new Error("Name was not given");
        }
        await updateUserProfile(fullName);
    }

    async function save() {
        state = "saving";
        let fileUpload: Promise<void> | null = null;
        if (imageFile) {
            fileUpload = updateProfilePicture(imageFile);
        }
        try {
            await Promise.all([saveData(), fileUpload]);
            currentUser = unwrap(await fetchUser(), "Expected fetchUser");
        } finally {
            state = "viewing";
        }
    }

    function cancel() {
        state = "viewing";
    }
</script>

<SettingsPage title="My Profile">
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

            <InputField
                style={{ kind: "field", inputType: "text" }}
                bind:value={fullName}
                name="full-name"
                placeholder={$_("user.profile.full-name.placeholder")}
            />
        </header>

        <SettingFooterEditSaveButtons bind:state {save} {cancel} />
    </div>
</SettingsPage>
