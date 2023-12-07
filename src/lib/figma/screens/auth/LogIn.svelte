<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { login } from "$lib/stores/user";
    import { signUpUrl, requestPasswordResetUrl } from "$lib/urls/user";

    export let redirectTo = "/dashboard";

    let email: string;
    let password: string;

    let error: string | undefined;

    async function action() {
        // TODO validate form
        error = undefined;
        try {
            await login(email, password, redirectTo, { fetch });
        } catch {
            // TODO set the error to something meaningful
            error = $_("auth.log-in.invalid-credentials");
        }
    }
</script>

<AuthScreen title={$_("auth.log-in.title")} {action}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.log-in.enter-your-email")}
            style={{ inputType: "email" }}
            name="email"
            label={$_("auth.log-in.email")}
            required
            bind:value={email}
        />
        <InputField
            placeholder={$_("auth.log-in.enter-your-password")}
            style={{ inputType: "password" }}
            name="password"
            label={$_("auth.log-in.password")}
            bind:value={password}
            required
            anchorBottom={{
                href: requestPasswordResetUrl,
                label: $_("auth.log-in.forgot-password"),
            }}
        />
        {#if error}
            <div>
                {error}
            </div>
        {/if}
        <Button
            action={{ kind: "button", action }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("auth.log-in.log-in")}
        />
        <div class="text-center">
            {$_("auth.log-in.no-account")}
            <Anchor
                href={signUpUrl}
                label={$_("auth.log-in.sign-up-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
