<script lang="ts">
    import { _ } from "svelte-i18n";
    import AuthScreen from "$lib/figma/screens/AuthScreen.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import Anchor from "$lib/figma/typography/Anchor.svelte";
    import { requestPasswordReset } from "$lib/stores/user";

    let email: string;

    async function submit() {
        await requestPasswordReset(email);
    }
</script>

<AuthScreen title={$_("request-password-reset.title")} action={submit}>
    {$_("request-password-reset.explanation")}
    <InputField
        placeholder={$_("request-password-reset.enter-your-email")}
        style={{ kind: "field", inputType: "text" }}
        name="email"
        label={$_("request-password-reset.email")}
        bind:value={email}
    />
    <Button
        on:click={submit}
        style={{ kind: "primary" }}
        color="blue"
        disabled={false}
        size="medium"
        label={$_("request-password-reset.send-reset-password-link")}
    />
    <div class="">
        <Anchor
            href="/signup"
            label={$_("request-password-reset.back-to-log-in")}
            size="normal"
        />
    </div>
</AuthScreen>
