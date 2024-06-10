<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023, 2024 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { logIn } from "$lib/stores/user";
    import type { FormViewState } from "$lib/types/ui";
    import { dashboardUrl } from "$lib/urls/dashboard";
    import { signUpUrl, requestPasswordResetUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { redirectTo } = data;

    let email: string | undefined = undefined;
    let emailValidation: InputFieldValidation | undefined = undefined;
    let password: string | undefined = undefined;
    let passwordValidation: InputFieldValidation | undefined = undefined;

    let state: FormViewState = { kind: "start" };

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
        const { error } = await logIn(email, password);
        if (error === undefined) {
            // TODO redirect to `/{redirectTo}` instead
            // To prevent users not being redirected to third parties
            // SvelteKit's goto sort of addresses this already, it would just
            // be cleaner to not have to only rely on SvelteKit's in-host goto
            // destination restriction
            await goto(redirectTo ?? dashboardUrl);
            return;
        } else if (error.code === 429) {
            state = {
                kind: "error",
                message: $_("auth.log-in.error.rate-limit"),
            };
            return;
        } else if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("auth.log-in.error.other", {
                    values: { error: JSON.stringify(error) },
                }),
            };
            return;
        }
        state = {
            kind: "error",
            message: $_("auth.log-in.error.credentials"),
        };
        const { details } = error;
        emailValidation = details.email
            ? { ok: false, error: details.email }
            : (emailValidation = {
                  ok: true,
                  result: $_("auth.log-in.email.valid"),
              });
        passwordValidation = details.password
            ? { ok: false, error: details.password }
            : (passwordValidation = { ok: true, result: "" });
    }
</script>

<svelte:head>
    <title>{$_("auth.log-in.title")}</title>
</svelte:head>

<AuthScreen title={$_("auth.log-in.heading")} {action}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.log-in.email.placeholder")}
            style={{ inputType: "email" }}
            name="email"
            label={$_("auth.log-in.email.label")}
            required
            bind:value={email}
            validation={emailValidation}
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
            validation={passwordValidation}
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
                ? $_("auth.log-in.submit.submitting")
                : $_("auth.log-in.submit.start")}
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
