<script lang="ts">
    import { _ } from "svelte-i18n";

    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { updateProfilePicture } from "$lib/repository/user";
    import { fetchUser, updateUserProfile } from "$lib/stores/user";
    import { unwrap } from "$lib/utils/type";

    import type { PageData } from "./$types";

    export let data: PageData;

    let { user } = data;
    let { full_name: fullName } = user;

    $: hasProfilePicture =
        imageFile !== undefined || user.profile_picture !== null;

    let state: "viewing" | "editing" | "saving" = "viewing";
    let imageFile: File | undefined = undefined;

    function fileSelected(file: File, src: string) {
        state = "editing";
        imageFile = file;
        user.profile_picture = src;
    }

    async function saveData() {
        if (!fullName) {
            throw new Error("Name was not given");
        }
        await updateUserProfile(fullName, { fetch });
    }

    async function save() {
        state = "saving";
        let fileUpload: Promise<void> | undefined = undefined;
        fileUpload = updateProfilePicture(imageFile);
        await Promise.all([saveData(), fileUpload]);
        user = unwrap(await fetchUser({ fetch }), "Expected fetchUser");
        // TODO show confirmation flash when saving complete Justus
        // 2023-08-03
        state = "viewing";
        imageFile = undefined;
    }

    function removePicture() {
        state = "editing";
        user.profile_picture = null;
        imageFile = undefined;
    }

    function cancel() {
        state = "viewing";
        fullName = user.full_name;
        user = data.user;
    }
</script>

<figure class="flex flex-col items-center gap-7">
    <div class="relative flex w-max flex-col">
        <AvatarVariant size="large" content={{ kind: "single", user }} />
        <div class="absolute -bottom-1/4 -right-1/4">
            <UploadAvatar
                {fileSelected}
                label={$_(
                    "user-account-settings.overview.profile-picture.prompt",
                )}
            />
        </div>
    </div>
    <figcaption>
        {$_("user-account-settings.overview.profile-picture.current")}
    </figcaption>
</figure>
<Button
    action={{
        kind: "button",
        action: removePicture,
        disabled: !hasProfilePicture || state === "saving",
    }}
    size="medium"
    color="blue"
    style={{ kind: "primary" }}
    label={$_("user-account-settings.overview.profile-picture.remove")}
/>
<div class="flex flex-col gap-10">
    <div class="flex flex-col gap-4">
        <InputField
            label={$_("user-account-settings.overview.full-name.label")}
            placeholder={$_(
                "user-account-settings.overview.full-name.placeholder",
            )}
            name="full_name"
            bind:value={fullName}
            style={{ inputType: "text" }}
            readonly={state !== "editing"}
            onClick={() => {
                state = "editing";
            }}
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
                    "Delete account not implemented",
                ),
            }}
            size="medium"
            color="red"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.delete-account")}
        />
        <Anchor
            href="/user/profile/change-password"
            size="normal"
            label={$_("user-account-settings.overview.change-password")}
        />
        <Anchor
            href="/user/profile/update-email"
            size="normal"
            label={$_("user-account-settings.overview.update-email")}
        />
    </div>
</div>
