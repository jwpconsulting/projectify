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

    let imageFile: File | undefined = undefined;

    export let user: User;

    let { full_name: fullName } = user;

    function fileSelected(file: File, src: string) {
        state = "editing";
        imageFile = file;
        user.profile_picture = src;
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
        await Promise.all([saveData(), fileUpload]);
        user = unwrap(await fetchUser({ fetch }), "Expected fetchUser");
        // TODO show confirmation flash when saving complete Justus
        // 2023-08-03
        state = "viewing";
    }

    function cancel() {
        state = "viewing";
    }
</script>

<figure class="flex flex-col items-center gap-7">
    <div class="relative flex w-max flex-col">
        <AvatarVariant size="large" content={{ kind: "single", user }} />
        <div class="absolute -bottom-1/4 -right-1/4">
            <UploadAvatar
                {fileSelected}
                label={$_(
                    "user-account-settings.overview.profile-picture.prompt"
                )}
            />
        </div>
    </div>
    <figcaption>
        {$_("user-account-settings.overview.profile-picture.current")}
    </figcaption>
</figure>
<div class="flex flex-col gap-10">
    <div class="flex flex-col gap-4">
        <InputField
            label={$_("user-account-settings.overview.full-name.label")}
            placeholder={$_(
                "user-account-settings.overview.full-name.placeholder"
            )}
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
                kind: "a",
                href: "/user/profile/change-password",
            }}
            size="medium"
            color="blue"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.change-password")}
        />
        <Button
            action={{
                kind: "a",
                href: "/user/profile/update-email",
            }}
            size="medium"
            color="blue"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.update-email")}
        />
    </div>
    <div class="flex flex-col gap-2">
        <Button
            action={{
                kind: "button",
                action: save,
                disabled: state !== "editing",
            }}
            size="medium"
            color="blue"
            style={{ kind: "primary" }}
            label={$_("user-account-settings.overview.save")}
        />
        <Button
            action={{
                kind: "button",
                action: cancel,
                disabled: state !== "editing",
            }}
            size="medium"
            color="blue"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.cancel")}
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
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.delete-account")}
        />
    </div>
</div>
