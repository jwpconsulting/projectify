<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;

    const hasBeenEdited = false;
    let currentPassword = "";
    let newEmail = "";
    // TODO wiring

    onMount(() => {
        console.log("TODO", user);
    });
</script>

<div class="flex flex-col items-center gap-12">
    <h1 class="text-2xl font-bold">
        {$_("user-account-settings.update-email.title")}
    </h1>
    <div class="flex w-full flex-col gap-10">
        <div class="flex flex-col gap-4">
            <InputField
                label={$_(
                    "user-account-settings.update-email.current-password.label"
                )}
                placeholder={$_(
                    "user-account-settings.update-email.current-password.placeholder"
                )}
                name="current-password"
                style={{ kind: "field", inputType: "password" }}
                bind:value={currentPassword}
            />
            <InputField
                label={$_(
                    "user-account-settings.update-email.new-email.label"
                )}
                placeholder={$_(
                    "user-account-settings.update-email.new-email.placeholder"
                )}
                name="new-email"
                style={{ kind: "field", inputType: "text" }}
                bind:value={newEmail}
            />
        </div>
        <div class="flex flex-row gap-2">
            <Button
                action={{
                    kind: "a",
                    href: "/user/profile",
                }}
                size="medium"
                color="blue"
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.update-email.cancel")}
            />
            <Button
                action={{
                    kind: "button",
                    action: console.error.bind(
                        null,
                        "Update email not implemented"
                    ),
                    disabled: hasBeenEdited,
                }}
                size="medium"
                color="blue"
                style={{ kind: "primary" }}
                label={$_("user-account-settings.update-email.save")}
            />
        </div>
    </div>
</div>
