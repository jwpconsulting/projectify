<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { goto } from "$lib/navigation";
    import { changePassword } from "$lib/repository/user";
    import type { AuthViewState } from "$lib/types/ui";
    import { getProfileUrl } from "$lib/urls";
    import { changedPasswordUrl } from "$lib/urls/user";

    let state: AuthViewState = { kind: "start" };

    let currentPassword: string | undefined = undefined;
    let currentPasswordValidation: InputFieldValidation | undefined =
        undefined;
    let newPassword1: string | undefined = undefined;
    let newPasswordValidation: InputFieldValidation | undefined = undefined;
    let newPassword2: string | undefined = undefined;

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
        const result = await changePassword(currentPassword, newPassword1, {
            fetch,
        });
        if (result.ok) {
            await goto(changedPasswordUrl);
            return;
        }
        if (result.error.current_password !== undefined) {
            currentPasswordValidation = {
                ok: false,
                error: result.error.current_password,
            };
        } else {
            currentPasswordValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.change-password.current-password.correct",
                ),
            };
        }
        if (result.error.new_password !== undefined) {
            newPasswordValidation = {
                ok: false,
                error: result.error.new_password,
            };
        } else {
            newPasswordValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.change-password.new-password.correct",
                ),
            };
        }
        if (currentPasswordValidation.ok && newPasswordValidation.ok) {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.change-password.validation.general-error",
                    { values: { detail: JSON.stringify(result.error) } },
                ),
            };
        } else {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.change-password.validation.field-errors",
                ),
            };
        }
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
