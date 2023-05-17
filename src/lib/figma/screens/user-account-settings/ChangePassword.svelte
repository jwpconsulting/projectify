<script lang="ts">
    import { _ } from "svelte-i18n";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";

    let hasBeenEdited = false;
    let currentPassword = "";
    let newPassword1 = "";
    let newPassword2 = "";
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
                size="medium"
                color="blue"
                disabled={false}
                style={{ kind: "secondary" }}
                label={$_("user-account-settings.cancel")}
            />
            <Button
                size="medium"
                color="blue"
                disabled={hasBeenEdited}
                style={{ kind: "primary" }}
                label={$_("user-account-settings.change-password")}
            />
        </div>
    </div>
</div>
