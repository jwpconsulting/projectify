<script lang="ts">
    import { _ } from "svelte-i18n";
    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
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
            on:click={submit}
            style={{ kind: "primary" }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("request-password-reset.send-reset-password-link")}
        />
        <div class="text-center">
            <Anchor
                href="/signup"
                label={$_("request-password-reset.return-to-log-in")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
