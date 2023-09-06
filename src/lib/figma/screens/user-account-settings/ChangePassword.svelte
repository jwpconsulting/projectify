<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;

    const hasBeenEdited = false;
    let currentPassword = "";
    let newPassword1 = "";
    let newPassword2 = "";

    onMount(() => {
        console.log("TODO", user);
    });
    // TODO wiring
</script>

<div class="flex flex-col items-center gap-12">
    <h1 class="text-2xl font-bold">
        {$_("user-account-settings.change-password.title")}
    </h1>
    <div class="flex w-full flex-col gap-10">
        <div class="flex flex-col gap-4">
            <InputField
                label={$_(
                    "user-account-settings.change-password.current-password.label"
                )}
                placeholder={$_(
                    "user-account-settings.change-password.current-password.placeholder"
                )}
                name="current-password"
                style={{ kind: "field", inputType: "password" }}
                bind:value={currentPassword}
            />
            <InputField
                label={$_(
                    "user-account-settings.change-password.new-password.label"
                )}
                placeholder={$_(
                    "user-account-settings.change-password.new-password.placeholder"
                )}
                name="new-password"
                style={{ kind: "field", inputType: "password" }}
                bind:value={newPassword1}
            />
            <InputField
                label={$_(
                    "user-account-settings.change-password.confirm-password.label"
                )}
                placeholder={$_(
                    "user-account-settings.change-password.confirm-password.placeholder"
                )}
                name="confirm-password"
                style={{ kind: "field", inputType: "password" }}
                bind:value={newPassword2}
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
                label={$_("user-account-settings.change-password.cancel")}
            />
            <Button
                action={{
                    kind: "button",
                    action: () => {
                        console.error("Change password not implemented");
                    },
                    disabled: !hasBeenEdited,
                }}
                size="medium"
                color="blue"
                style={{ kind: "primary" }}
                label={$_("user-account-settings.change-password.save")}
            />
        </div>
    </div>
</div>
