<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { User } from "$lib/types/user";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";

    export let user: User;
    const hasBeenEdited = false;
</script>

<div class="flex flex-col gap-12 rounded-lg bg-foreground p-4">
    <figure class="flex flex-col items-center gap-7">
        <div class="relative flex w-max flex-col">
            <AvatarVariant size="large" content={{ kind: "single", user }} />
            <div class="absolute -right-1/4 -bottom-1/4">
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
                style={{ kind: "field", inputType: "text" }}
            />
            <Button
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.change-password")}
            />
            <Button
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.update-email")}
            />
        </div>
        <div class="flex flex-col gap-2">
            <Button
                size="medium"
                color="blue"
                disabled={hasBeenEdited}
                style={{ kind: "primary" }}
                label={$_("user-account-settings.save-changes")}
            />
            <Button
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.cancel")}
            />
            <Button
                size="medium"
                color="red"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.delete-account")}
            />
        </div>
    </div>
</div>
