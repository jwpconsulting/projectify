<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { login } from "$lib/stores/user";

    export let redirectTo = "/dashboard";

    let email: string;
    let password: string;

    let error: string | undefined;

    async function action() {
        // TODO validate form
        error = undefined;
        try {
            await login(email, password, redirectTo);
        } catch {
            error = $_("log-in.invalid-credentials");
        }
    }
</script>

<AuthScreen title={$_("log-in.title")} {action}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("log-in.enter-your-email")}
            style={{ kind: "field", inputType: "email" }}
            name="email"
            label={$_("log-in.email")}
            required
            bind:value={email}
        />
        <InputField
            placeholder={$_("log-in.enter-your-password")}
            style={{ kind: "field", inputType: "password" }}
            name="password"
            label={$_("log-in.password")}
            bind:value={password}
            required
            anchorBottom={{
                href: "/user/reset",
                label: $_("log-in.forgot-password"),
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
            disabled={false}
            size="medium"
            label={$_("log-in.log-in")}
        />
        <div class="text-center">
            {$_("log-in.no-account")}
            <Anchor
                href="/signup"
                label={$_("log-in.sign-up-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
