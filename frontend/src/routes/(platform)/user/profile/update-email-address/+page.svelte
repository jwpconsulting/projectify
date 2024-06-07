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
    import type { FormViewState } from "$lib/types/ui";
    import { getProfileUrl } from "$lib/urls";
    import {
        getLogInWithNextUrl,
        requestedEmailAddressUpdateUrl,
        updateEmailAddressUrl,
    } from "$lib/urls/user";

    import type { PageData } from "./$types";
    import { openApiClient } from "$lib/repository/util";

    export let data: PageData;

    const {
        user: { email },
    } = data;

    let state: FormViewState = { kind: "start" };

    let newEmail: string | undefined = undefined;
    let newEmailValidation: InputFieldValidation | undefined = undefined;
    let password: string | undefined = undefined;
    let passwordValidation: InputFieldValidation | undefined = undefined;

    async function submit() {
        if (newEmail === undefined) {
            throw new Error("Expected newEmail");
        }
        if (password === undefined) {
            throw new Error("Expected currentPassword");
        }
        const { error } = await openApiClient.POST(
            "/user/user/email-address-update/request",
            { body: { new_email: newEmail, password } },
        );

        if (error === undefined) {
            await goto(requestedEmailAddressUpdateUrl);
            return;
        }
        if (error.code === 429) {
            throw new Error("Too many request");
        }
        if (error.code === 403) {
            await goto(getLogInWithNextUrl(updateEmailAddressUrl));
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.update-email-address.error.general",
                ),
            };
            return;
        }
        const { details } = error;
        if (details.password === undefined) {
            passwordValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.update-email-address.current-password.valid",
                ),
            };
        } else {
            passwordValidation = {
                ok: false,
                error: details.password,
            };
        }
        if (details.new_email === undefined) {
            newEmailValidation = {
                ok: true,
                result: $_(
                    "user-account-settings.update-email-address.new-email.valid",
                ),
            };
        } else {
            newEmailValidation = {
                ok: false,
                error: details.new_email,
            };
        }
        state = {
            kind: "error",
            message: $_(
                "user-account-settings.update-email-address.error.field",
            ),
        };
    }
</script>

<h1 class="text-center text-2xl font-bold">
    {$_("user-account-settings.update-email-address.title")}
</h1>
<form class="flex w-full flex-col gap-10" on:submit|preventDefault={submit}>
    <div class="flex flex-col gap-4">
        <p>
            {$_("user-account-settings.update-email-address.current-email", {
                values: { email },
            })}
        </p>
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
        <InputField
            label={$_(
                "user-account-settings.update-email-address.current-password.label",
            )}
            placeholder={$_(
                "user-account-settings.update-email-address.current-password.placeholder",
            )}
            name="current-password"
            style={{ inputType: "password" }}
            bind:value={password}
            validation={passwordValidation}
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
