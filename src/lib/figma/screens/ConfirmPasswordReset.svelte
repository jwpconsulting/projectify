<script lang="ts">
    import { _ } from "svelte-i18n";
    import AuthScreen from "$lib/figma/screens/AuthScreen.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import { confirmPasswordReset } from "$lib/stores/user";

    export let email: string;
    export let token: string;
    let newPassword1: string;
    let newPassword2: string;

    async function submit() {
        await confirmPasswordReset(email, token, newPassword1);
    }
</script>

<AuthScreen title={$_("confirm-password-reset.title")} action={submit}>
    <InputField
        placeholder={$_("confirm-password-reset.enter-new-password")}
        style={{ kind: "field", inputType: "password" }}
        name="password1"
        label={$_("confirm-password-reset.new-password")}
        bind:value={newPassword1}
    />
    <InputField
        placeholder={$_("confirm-password-reset.confirm-new-password")}
        style={{ kind: "field", inputType: "text" }}
        name="password2"
        label={$_("confirm-password-reset.confirm-new-password")}
        bind:value={newPassword2}
    />
    <Button
        on:click={submit}
        style={{ kind: "primary" }}
        color="blue"
        disabled={false}
        size="medium"
        label={$_("confirm-password-reset.reset-password")}
    />
</AuthScreen>
