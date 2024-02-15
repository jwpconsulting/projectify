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
    import { requestEmailAddressUpdate } from "$lib/repository/user";
    import type { AuthViewState } from "$lib/types/ui";
    import { getProfileUrl } from "$lib/urls";
    import { requestedEmailAddressUpdateUrl } from "$lib/urls/user";

    let state: AuthViewState = { kind: "start" };

    let currentPassword: string | undefined = undefined;
    let currentPasswordValidation: InputFieldValidation | undefined =
        undefined;
    let newEmail: string | undefined = undefined;
    let newEmailValidation: InputFieldValidation | undefined = undefined;

    async function submit() {
        if (currentPassword === undefined) {
            throw new Error("Expected currentPassword");
        }
        if (newEmail === undefined) {
            throw new Error("Expected newEmail");
        }
        const response = await requestEmailAddressUpdate(
            currentPassword,
            newEmail,
            { fetch },
        );
        if (response.ok) {
            await goto(requestedEmailAddressUpdateUrl);
            return;
        }
        if (response.error.new_email === undefined) {
            newEmailValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.update-email-address.new-email.valid",
                ),
            };
        } else {
            newEmailValidation = {
                ok: false,
                error: response.error.new_email,
            };
        }
        if (response.error.password === undefined) {
            currentPasswordValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.update-email-address.current-password.valid",
                ),
            };
        } else {
            currentPasswordValidation = {
                ok: false,
                error: response.error.password,
            };
        }
        if (newEmailValidation.ok && currentPasswordValidation.ok) {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.update-email-address.error.general",
                ),
            };
        } else {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.update-email-address.error.field",
                ),
            };
        }
    }
</script>

<h1 class="text-center text-2xl font-bold">
    {$_("user-account-settings.update-email-address.title")}
</h1>
<form class="flex w-full flex-col gap-10" on:submit|preventDefault={submit}>
    <div class="flex flex-col gap-4">
        <InputField
            label={$_(
                "user-account-settings.update-email-address.current-password.label",
            )}
            placeholder={$_(
                "user-account-settings.update-email-address.current-password.placeholder",
            )}
            name="current-password"
            style={{ inputType: "password" }}
            bind:value={currentPassword}
            validation={currentPasswordValidation}
            required
        />
        <InputField
            label={$_(
                "user-account-settings.update-email-address.new-email.label",
            )}
            placeholder={$_(
                "user-account-settings.update-email-address.new-email.placeholder",
            )}
            name="new-email"
            style={{ inputType: "email" }}
            bind:value={newEmail}
            validation={newEmailValidation}
            required
        />
        {#if state.kind === "error"}
            <p>{state.message}</p>
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
            label={$_("user-account-settings.update-email-address.cancel")}
        />
        <Button
            action={{
                kind: "submit",
                disabled: state.kind === "submitting",
            }}
            size="medium"
            color="blue"
            style={{ kind: "primary" }}
            label={$_("user-account-settings.update-email-address.save")}
        />
    </div>
</form>
