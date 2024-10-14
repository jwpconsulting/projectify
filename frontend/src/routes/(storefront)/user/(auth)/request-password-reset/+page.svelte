<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { FormViewState } from "$lib/types/ui";
    import { requestedPasswordResetUrl } from "$lib/urls/user";

    import { goto } from "$app/navigation";
    import { openApiClient } from "$lib/repository/util";

    let email: string | undefined = undefined;
    let emailValidation: InputFieldValidation | undefined = undefined;

    let state: FormViewState = { kind: "start" };

    async function submit() {
        if (!email) {
            throw new Error("Expected email");
        }
        state = { kind: "submitting" };
        const { error } = await openApiClient.POST(
            "/user/user/request-password-reset",
            { body: { email } },
        );
        if (error === undefined) {
            await goto(requestedPasswordResetUrl);
            return;
        }
        if (error.code === 429) {
            state = {
                kind: "error",
                message: $_(
                    "auth.request-password-reset.error.too-many-requests",
                ),
            };
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("auth.request-password-reset.error.generic"),
            };
            return;
        }
        const { details } = error;
        emailValidation = details.email
            ? { ok: false, error: details.email }
            : undefined;

        state = {
            kind: "error",
            message: $_("auth.request-password-reset.error.validation"),
        };
    }
</script>

<svelte:head>
    <title>{$_("auth.request-password-reset.title")}</title>
</svelte:head>

<AuthScreen title={$_("auth.request-password-reset.heading")} action={submit}>
    <div class="text-center">
        {$_("auth.request-password-reset.explanation")}
    </div>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.request-password-reset.email.placeholder")}
            style={{ inputType: "email" }}
            name="email"
            label={$_("auth.request-password-reset.email.label")}
            bind:value={email}
            validation={emailValidation}
            required
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
            label={state.kind === "submitting"
                ? $_("auth.request-password-reset.submit.submitting")
                : $_("auth.request-password-reset.submit.start")}
        />
        <div class="text-center">
            <Anchor
                href="/user/sign-up"
                label={$_("auth.request-password-reset.return-to-log-in")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
