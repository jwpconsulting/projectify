<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { signUp } from "$lib/repository/user";
    import type { AuthViewState } from "$lib/types/ui";
    import { logInUrl, sentEmailConfirmationLinkUrl } from "$lib/urls/user";

    let email: string | undefined = undefined;
    let password: string | undefined = undefined;
    let tosAgreed: boolean | undefined = undefined;
    let privacyPolicyAgreed: boolean | undefined = undefined;

    let state: AuthViewState = { kind: "start" };

    async function action() {
        state = { kind: "submitting" };
        if (!email) {
            state = {
                kind: "error",
                message: $_("auth.sign-up.email.missing"),
            };
            return;
        }
        if (!password) {
            state = {
                kind: "error",
                message: $_("auth.sign-up.password.missing"),
            };
            return;
        }
        if (!tosAgreed) {
            state = { kind: "error", message: $_("auth.sign-up.tos.missing") };
            return;
        }
        if (!privacyPolicyAgreed) {
            state = {
                kind: "error",
                message: $_("auth.sign-up.privacy-policy.missing"),
            };
            return;
        }
        // TODO form validation
        try {
            // TODO show actual server error to user here
            await signUp(email, password, tosAgreed, privacyPolicyAgreed, {
                fetch,
            });
        } catch {
            state = {
                kind: "error",
                message: $_("auth.sign-up.generic-error"),
            };
            return;
        }
        await goto(sentEmailConfirmationLinkUrl);
    }
</script>

<AuthScreen
    title={$_("auth.sign-up.title")}
    {action}
    subTitle={$_("auth.sign-up.sub-title")}
>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.sign-up.email.placeholder")}
            style={{ inputType: "text" }}
            name="email"
            label={$_("auth.sign-up.email.label")}
            bind:value={email}
            required
        />
        <InputField
            placeholder={$_("auth.sign-up.password.placeholder")}
            style={{ inputType: "password" }}
            name="password"
            label={$_("auth.sign-up.password.label")}
            bind:value={password}
            required
        />
        <!-- XXX false positive -->
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={tosAgreed}
                disabled={false}
                contained={false}
                required
            />
            <span class="prose">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $_("auth.sign-up.tos.label", {
                    values: {
                        tosUrl: "/tos",
                    },
                })}</span
            >
        </label>
        <!-- XXX false positive -->
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={privacyPolicyAgreed}
                disabled={false}
                contained={false}
                required
            />
            <span class="prose">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $_("auth.sign-up.privacy-policy.label", {
                    values: {
                        privacyPolicyUrl: "/privacy",
                    },
                })}</span
            >
        </label>
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
            label={state.kind === "submitting"
                ? $_("auth.sign-up.submit.submitting")
                : $_("auth.sign-up.submit.ready")}
        />
        <div class="text-center">
            {$_("auth.sign-up.already-have-an-account")}
            <Anchor
                href={logInUrl}
                label={$_("auth.sign-up.log-in-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
