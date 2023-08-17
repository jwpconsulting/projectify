<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    let hasBeenEdited = false;
    let currentPassword = "";
    let newEmail = "";
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
                label={$_("user-account-settings.new-email")}
                placeholder={$_("user-account-settings.enter-new-email")}
                name="new-email"
                style={{ kind: "field", inputType: "text" }}
                bind:value={newEmail}
            />
        </div>
        <div class="flex flex-row gap-2">
            <Button
                action={{
                    kind: "button",
                    action: console.error.bind(null, "Cancel not implemented"),
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
                    action: console.error.bind(
                        null,
                        "Update email not implemented"
                    ),
                }}
                size="medium"
                color="blue"
                disabled={hasBeenEdited}
                style={{ kind: "primary" }}
                label={$_("user-account-settings.update-email")}
            />
        </div>
    </div>
</div>
