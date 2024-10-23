<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { goto } from "$lib/navigation";
    import type { FormViewState } from "$lib/types/ui";
    import { getProfileUrl } from "$lib/urls";
    import {
        changePasswordUrl,
        changedPasswordUrl,
        getLogInWithNextUrl,
    } from "$lib/urls/user";
    import { openApiClient } from "$lib/repository/util";
    import { onMount } from "svelte";

    let state: FormViewState = { kind: "start" };

    let currentPassword: string | undefined = undefined;
    let currentPasswordValidation: InputFieldValidation | undefined =
        undefined;
    let newPassword1: string | undefined = undefined;
    let newPasswordValidation: InputFieldValidation | undefined = undefined;
    let newPassword2: string | undefined = undefined;

    let passwordPolicies: string[] | undefined = undefined;
    onMount(async () => {
        const response = await openApiClient.GET("/user/user/password-policy");
        if (response.data === undefined) {
            throw new Error("Could not get password policies");
        }
        passwordPolicies = response.data.policies;
    });

    $: canSubmit = state.kind !== "submitting";

    async function submit() {
        if (currentPassword === undefined) {
            throw new Error("Expected currentPassword");
        }
        if (newPassword1 === undefined) {
            throw new Error("Expected newPassword1");
        }
        if (newPassword2 === undefined) {
            throw new Error("Expected newPassword2");
        }
        if (newPassword1 !== newPassword2) {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.change-password.validation.must-match",
                ),
            };
            return;
        }
        state = { kind: "submitting" };
        const { error } = await openApiClient.POST(
            "/user/user/change-password",
            {
                body: {
                    current_password: currentPassword,
                    new_password: newPassword1,
                },
            },
        );
        if (error === undefined) {
            await goto(changedPasswordUrl);
            return;
        }
        if (error.code === 429) {
            // TODO handle this
            throw new Error("Too many request");
        }
        if (error.code === 403) {
            await goto(getLogInWithNextUrl(changePasswordUrl));
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.change-password.validation.general-error",
                    { values: { details: JSON.stringify(error) } },
                ),
            };
            return;
        }
        const { details } = error;
        if (details.current_password !== undefined) {
            currentPasswordValidation = {
                ok: false,
                error: details.current_password,
            };
        } else {
            currentPasswordValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.change-password.current-password.correct",
                ),
            };
        }
        if (details.new_password !== undefined) {
            newPasswordValidation = { ok: false, error: details.new_password };
        } else {
            newPasswordValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.change-password.new-password.correct",
                ),
            };
        }
        state = {
            kind: "error",
            message: $_(
                "user-account-settings.change-password.validation.field-errors",
            ),
        };
    }
</script>

<h1 class="text-center text-2xl font-bold">
    {$_("user-account-settings.change-password.title")}
</h1>
<form on:submit|preventDefault={submit} class="flex w-full flex-col gap-10">
    <div class="flex flex-col gap-4">
        <InputField
            label={$_(
                "user-account-settings.change-password.current-password.label",
            )}
            placeholder={$_(
                "user-account-settings.change-password.current-password.placeholder",
            )}
            name="current-password"
            style={{ inputType: "password" }}
            bind:value={currentPassword}
            required
            validation={currentPasswordValidation}
        />
        <InputField
            label={$_(
                "user-account-settings.change-password.new-password.label",
            )}
            placeholder={$_(
                "user-account-settings.change-password.new-password.placeholder",
            )}
            name="new-password"
            style={{ inputType: "password" }}
            bind:value={newPassword1}
            required
            validation={newPasswordValidation}
        />
        <InputField
            label={$_(
                "user-account-settings.change-password.confirm-password.label",
            )}
            placeholder={$_(
                "user-account-settings.change-password.confirm-password.placeholder",
            )}
            name="confirm-password"
            style={{ inputType: "password" }}
            bind:value={newPassword2}
            required
            validation={newPasswordValidation}
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
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
        {/if}
    </div>
    <div class="flex flex-row gap-2">
        <Button
            action={{
                kind: "a",
                href: getProfileUrl(),
            }}
            size="medium"
            color="blue"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.change-password.cancel")}
        />
        <Button
            action={{
                kind: "submit",
                disabled: !canSubmit,
            }}
            size="medium"
            color="blue"
            style={{ kind: "primary" }}
            label={state.kind === "submitting"
                ? $_("user-account-settings.change-password.submit.submitting")
                : $_("user-account-settings.change-password.submit.start")}
        />
    </div>
</form>
