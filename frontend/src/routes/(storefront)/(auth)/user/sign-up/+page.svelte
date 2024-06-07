<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import type { FormViewState } from "$lib/types/ui";
    import { logInUrl, sentEmailConfirmationLinkUrl } from "$lib/urls/user";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { openApiClient } from "$lib/repository/util";
    import { onMount } from "svelte";

    let email: string | undefined = undefined;
    let emailValidation: InputFieldValidation | undefined = undefined;

    let password: string | undefined = undefined;
    let passwordValidation: InputFieldValidation | undefined = undefined;

    let tosAgreed: boolean | undefined = undefined;
    let privacyPolicyAgreed: boolean | undefined = undefined;

    let state: FormViewState = { kind: "start" };

    // Load password policies
    let passwordPolicies: string[] | undefined = undefined;
    onMount(async () => {
        const response = await openApiClient.GET("/user/user/password-policy");
        if (response.data === undefined) {
            throw new Error("Could not get password policies");
        }
        passwordPolicies = response.data.policies;
    });

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
        const { error } = await openApiClient.POST("/user/user/sign-up", {
            body: {
                email,
                password,
                tos_agreed: tosAgreed,
                privacy_policy_agreed: privacyPolicyAgreed,
            },
            fetch,
        });
        if (error === undefined) {
            await goto(sentEmailConfirmationLinkUrl);
            return;
        }
        if (error.code === 429) {
            state = {
                kind: "error",
                message: $_("auth.sign-up.error.too-many-requests"),
            };
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("auth.sign-up.error.generic"),
            };
            return;
        }
        const { details } = error;
        emailValidation = undefined;
        passwordValidation = undefined;
        if (details.email) {
            emailValidation = { ok: false, error: details.email };
        } else {
            emailValidation = {
                ok: true,
                result: $_("auth.sign-up.email.valid"),
            };
        }
        if (details.password !== undefined) {
            passwordValidation = { ok: false, error: details.password };
        } else {
            passwordValidation = {
                ok: true,
                result: $_("auth.sign-up.password.valid"),
            };
        }
        state = {
            kind: "error",
            message: $_("auth.sign-up.error.field"),
        };
    }
</script>

<svelte:head>
    <title>{$_("auth.sign-up.title")}</title>
</svelte:head>

<AuthScreen
    title={$_("auth.sign-up.heading")}
    {action}
    subTitle={$_("auth.sign-up.sub-heading")}
>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.sign-up.email.placeholder")}
            style={{ inputType: "text" }}
            name="email"
            label={$_("auth.sign-up.email.label")}
            bind:value={email}
            required
            validation={emailValidation}
        />
        <section class="flex flex-col gap-2">
            <InputField
                placeholder={$_("auth.sign-up.password.placeholder")}
                style={{ inputType: "password" }}
                name="password"
                label={$_("auth.sign-up.password.label")}
                bind:value={password}
                required
                validation={passwordValidation}
            />
            {#if passwordPolicies}
                <header class="font-bold">
                    {$_("auth.sign-up.password.policies")}
                </header>
                <ul class="flex list-inside list-disc flex-col gap-0.5">
                    {#each passwordPolicies as policy}
                        <li>{policy}</li>
                    {/each}
                </ul>
            {/if}
        </section>
        <!-- XXX false positive -->
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={tosAgreed}
                disabled={false}
                contained={false}
                required
            />
            <Anchor
                label={$_("auth.sign-up.tos.label")}
                href="/tos"
                size="normal"
                openBlank
            />
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
            <Anchor
                label={$_("auth.sign-up.privacy-policy.label")}
                href="/privacy"
                size="normal"
                openBlank
            />
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
