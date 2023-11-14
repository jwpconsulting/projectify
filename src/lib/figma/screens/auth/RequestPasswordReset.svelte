<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { requestPasswordReset } from "$lib/stores/user";

    let email: string;

    async function submit() {
        // TODO do some kind of validation here
        await requestPasswordReset(email);
    }
</script>

<AuthScreen title={$_("request-password-reset.title")} action={submit}>
    <div class="text-center">
        {$_("request-password-reset.explanation")}
    </div>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("request-password-reset.enter-your-email")}
            style={{ kind: "field", inputType: "text" }}
            name="email"
            label={$_("request-password-reset.email")}
            bind:value={email}
        />
        <Button
            action={{ kind: "button", action: submit }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("request-password-reset.send-reset-password-link")}
        />
        <div class="text-center">
            <Anchor
                href="/user/sign-up"
                label={$_("request-password-reset.return-to-log-in")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
