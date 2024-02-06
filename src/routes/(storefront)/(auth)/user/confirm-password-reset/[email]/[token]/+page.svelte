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
    import { confirmPasswordReset } from "$lib/repository/user";
    import type { AuthViewState } from "$lib/types/ui";
    import { requestPasswordResetUrl, resetPasswordUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;

    let state: AuthViewState = { kind: "start" };

    const { email, token } = data;
    let password1: string | undefined = undefined;
    let password1Validation: InputFieldValidation | undefined = undefined;
    let password2: string | undefined = undefined;
    let password2Validation: InputFieldValidation | undefined = undefined;

    async function submit() {
        if (password1 === undefined) {
            throw new Error("Expected password1");
        }
        if (password2 === undefined) {
            throw new Error("Expected password1");
        }
        if (password1 !== password2) {
            state = {
                kind: "error",
                message: $_("auth.confirm-password-reset.validation.no-match"),
            };
            password1Validation = {
                ok: false,
                error: $_(
                    "auth.confirm-password-reset.password-1.validation.no-match",
                ),
            };
            password2Validation = {
                ok: false,
                error: $_(
                    "auth.confirm-password-reset.password-2.validation.no-match",
                ),
            };
            return;
        }
        password1Validation = password2Validation = undefined;
        state = { kind: "submitting" };
        const result = await confirmPasswordReset(email, token, password1, {
            fetch,
        });
        if (result.ok) {
            await goto(resetPasswordUrl);
            return;
        }
        console.error("Error resetting password", result.error);
        if (result.error.new_password) {
            password1Validation = {
                ok: false,
                error: result.error.new_password,
            };
        }
        state = {
            kind: "error",
            message: $_("auth.confirm-password-reset.error"),
        };
    }
</script>

<AuthScreen title={$_("auth.confirm-password-reset.title")} action={submit}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_(
                "auth.confirm-password-reset.password-1.placeholder",
            )}
            style={{ inputType: "password" }}
            name="password-1"
            label={$_("auth.confirm-password-reset.password-1.label")}
            bind:value={password1}
            validation={password1Validation}
            required
        />
        <InputField
            placeholder={$_(
                "auth.confirm-password-reset.password-2.placeholder",
            )}
            style={{ inputType: "password" }}
            name="password-2"
            label={$_("auth.confirm-password-reset.password-2.label")}
            bind:value={password2}
            validation={password2Validation}
            required
        />
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
            <Anchor
                label={$_(
                    "auth.confirm-password-reset.request-password-reset",
                )}
                href={requestPasswordResetUrl}
                size="normal"
            />
        {/if}
        <Button
            action={{
                kind: "submit",
                disabled: state.kind === "submitting",
            }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={state.kind == "submitting"
                ? $_("auth.confirm-password-reset.submit.submitting")
                : state.kind === "error"
                ? $_("auth.confirm-password-reset.submit.error")
                : $_("auth.confirm-password-reset.submit.start")}
        />
    </div>
</AuthScreen>
