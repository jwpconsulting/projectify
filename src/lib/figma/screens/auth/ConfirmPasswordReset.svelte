<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { confirmPasswordReset } from "$lib/stores/user";
    import { logInUrl } from "$lib/urls/user";

    export let email: string;
    export let token: string;
    // TODO should be string | undefined
    let newPassword1: string;
    let newPassword2: string;

    async function submit() {
        // TODO validate form
        // TODO show error
        try {
            await confirmPasswordReset(email, token, newPassword1);
            await goto(logInUrl);
        } catch (error) {
            console.error("password reset went wrong", error);
            throw error;
        }
    }
</script>

<AuthScreen title={$_("auth.confirm-password-reset.title")} action={submit}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.confirm-password-reset.enter-new-password")}
            style={{ kind: "field", inputType: "password" }}
            name="password1"
            label={$_("auth.confirm-password-reset.new-password")}
            bind:value={newPassword1}
        />
        <InputField
            placeholder={$_(
                "auth.confirm-password-reset.confirm-new-password"
            )}
            style={{ kind: "field", inputType: "password" }}
            name="password2"
            label={$_("auth.confirm-password-reset.confirm-new-password")}
            bind:value={newPassword2}
        />
        <Button
            action={{ kind: "button", action: submit }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("auth.confirm-password-reset.reset-password")}
        />
    </div>
</AuthScreen>
