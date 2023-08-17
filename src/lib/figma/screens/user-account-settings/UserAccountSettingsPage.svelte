<script lang="ts">
    import { _ } from "svelte-i18n";

    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateProfilePicture } from "$lib/repository/user";
    import { fetchUser, updateUserProfile } from "$lib/stores/user";
    import type { User } from "$lib/types/user";
    import { unwrap } from "$lib/utils/type";

    let state: "viewing" | "editing" | "saving" = "viewing";

    let imageFile: File | null = null;

    export let user: User;

    let { full_name: fullName } = user;

    // TODO
    // import UserProfilePicture from "$lib/components/userProfilePicture.svelte";
    // import ProfilePictureFileSelector from "$lib/components/profilePictureFileSelector.svelte";
    // function onFileSelected({
    //     detail: { src, file },
    // }: {
    //     detail: { src: string; file: File };
    // }) {
    //     imageFile = file;
    //     state = "editing";
    //     user.profile_picture = src;
    // }

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
        console.log(user);
        await Promise.all([saveData(), fileUpload]);
        user = unwrap(await fetchUser(), "Expected fetchUser");
        // TODO show confirmation flash when saving complete Justus
        // 2023-08-03
        state = "viewing";
        console.log(user);
    }

    function cancel() {
        state = "viewing";
    }
</script>

<div class="flex flex-col gap-12 rounded-lg bg-foreground p-4">
    <!--

            <ProfilePictureFileSelector
                url={user.profile_picture}
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
-->
    <figure class="flex flex-col items-center gap-7">
        <div class="relative flex w-max flex-col">
            <AvatarVariant size="large" content={{ kind: "single", user }} />
            <div class="absolute -bottom-1/4 -right-1/4">
                <UploadAvatar />
            </div>
        </div>
        <figcaption>
            {$_("user-account-settings.your-current-avatar")}
        </figcaption>
    </figure>
    <div class="flex flex-col gap-10">
        <div class="flex flex-col gap-4">
            <InputField
                label={$_("user-account-settings.name")}
                placeholder={$_("user-account-settings.enter-your-full-name")}
                name="full_name"
                bind:value={fullName}
                style={{ kind: "field", inputType: "text" }}
                readonly={state !== "editing"}
                onClick={() => {
                    state = "editing";
                }}
            />
            <Button
                action={{
                    kind: "button",
                    action: console.error.bind(
                        null,
                        "Change password not implemented"
                    ),
                }}
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.change-password")}
            />
            <Button
                action={{
                    kind: "button",
                    action: console.error.bind(
                        null,
                        "Update email not implemented"
                    ),
                }}
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.update-email")}
            />
        </div>
        <div class="flex flex-col gap-2">
            <Button
                action={{
                    kind: "button",
                    action: save,
                }}
                size="medium"
                color="blue"
                disabled={state !== "editing"}
                style={{ kind: "primary" }}
                label={$_("user-account-settings.save-changes")}
            />
            <Button
                action={{
                    kind: "button",
                    action: cancel,
                }}
                size="medium"
                color="blue"
                disabled={state !== "editing"}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.cancel")}
            />
            <Button
                action={{
                    kind: "button",
                    action: console.error.bind(
                        null,
                        "Delete account not implemented"
                    ),
                }}
                size="medium"
                color="red"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.delete-account")}
            />
        </div>
    </div>
</div>
