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
        user = unwrap(await fetchUser(), "Expected fetchUser");
        // TODO show confirmation flash when saving complete Justus
        // 2023-08-03
        state = "viewing";
    }

    function cancel() {
        state = "viewing";
    }
</script>

<div class="flex flex-col gap-12 rounded-lg bg-foreground p-4">
    <figure class="flex flex-col items-center gap-7">
        <div class="relative flex w-max flex-col">
            <AvatarVariant size="large" content={{ kind: "single", user }} />
            <div class="absolute -bottom-1/4 -right-1/4">
                <UploadAvatar {fileSelected} />
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
                    kind: "a",
                    href: "/user/profile/change-password",
                }}
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.change-password")}
            />
            <Button
                action={{
                    kind: "a",
                    href: "/user/profile/update-email",
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
