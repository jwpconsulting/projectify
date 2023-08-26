<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;

    let hasBeenEdited = false;
    let currentPassword = "";
    let newPassword1 = "";
    let newPassword2 = "";

    onMount(() => {
        console.log("TODO", user);
    });
    // TODO wiring
</script>

<div class="flex flex-col gap-12">
    <h1>{$_("user-account-settings.change-password")}</h1>
    <div class="flex flex-col gap-10">
        <div class="flex flex-col gap-4">
            <InputField
                label={$_("user-account-settings.current-password")}
                placeholder={$_("user-account-settings.enter-password")}
                name="current-password"
                style={{ kind: "field", inputType: "password" }}
                bind:value={currentPassword}
            />
            <InputField
                label={$_("user-account-settings.new-password")}
                placeholder={$_("user-account-settings.enter-new-password")}
                name="new-password-1"
                style={{ kind: "field", inputType: "password" }}
                bind:value={newPassword1}
            />
            <InputField
                label={$_("user-account-settings.confirm-password")}
                placeholder={$_("user-account-settings.confirm-new-password")}
                name="new-password-2"
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
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.cancel")}
            />
            <Button
                action={{
                    kind: "button",
                    action: () => {
                        console.error("Change password not implemented");
                    },
                }}
                size="medium"
                color="blue"
                disabled={hasBeenEdited}
                style={{ kind: "primary" }}
                label={$_("user-account-settings.change-password")}
            />
        </div>
    </div>
</div>
