<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { login } from "$lib/stores/user";
    import { signUpUrl, requestPasswordResetUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { redirectTo } = data;

    let email: string | undefined = undefined;
    let password: string | undefined = undefined;

    type State =
        | { kind: "start" }
        | { kind: "submitting" }
        | { kind: "error"; message: string };

    let state: State = { kind: "start" };

    async function action() {
        state = { kind: "submitting" };
        if (!email) {
            state = {
                kind: "error",
                message: $_("auth.log-in.email.missing"),
            };
            return;
        }
        if (!password) {
            state = {
                kind: "error",
                message: $_("auth.log-in.password.missing"),
            };
            return;
        }
        try {
            await login(email, password, redirectTo, { fetch });
        } catch {
            // TODO set the error to something meaningful
            state = {
                kind: "error",
                message: $_("auth.log-in.invalid-credentials"),
            };
        }
    }
</script>

<AuthScreen title={$_("auth.log-in.title")} {action}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.log-in.email.placeholder")}
            style={{ inputType: "email" }}
            name="email"
            label={$_("auth.log-in.email.label")}
            required
            bind:value={email}
        />
        <InputField
            placeholder={$_("auth.log-in.password.placeholder")}
            style={{ inputType: "password" }}
            name="password"
            label={$_("auth.log-in.password.label")}
            bind:value={password}
            required
            anchorBottom={{
                href: requestPasswordResetUrl,
                label: $_("auth.log-in.forgot-password"),
            }}
        />
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
        {/if}
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
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
