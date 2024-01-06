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
    import { goto } from "$lib/navigation";
    import { confirmPasswordReset } from "$lib/repository/user";
    import { logInUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { email, token } = data;
    // TODO should be string | undefined
    let newPassword1: string;
    let newPassword2: string;

    async function submit() {
        // TODO validate form
        // TODO show error
        try {
            await confirmPasswordReset(email, token, newPassword1, { fetch });
            await goto(logInUrl);
        } catch (error) {
            console.error("password reset went wrong", error);
            throw error;
        }
    }
</script>

<AuthScreen title={$_("auth.confirm-password-reset.title")} action={submit}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.confirm-password-reset.enter-new-password")}
            style={{ inputType: "password" }}
            name="password1"
            label={$_("auth.confirm-password-reset.new-password")}
            bind:value={newPassword1}
        />
        <InputField
            placeholder={$_(
                "auth.confirm-password-reset.confirm-new-password",
            )}
            style={{ inputType: "password" }}
            name="password2"
            label={$_("auth.confirm-password-reset.confirm-new-password")}
            bind:value={newPassword2}
        />
        <Button
            action={{ kind: "button", action: submit }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("auth.confirm-password-reset.reset-password")}
        />
    </div>
</AuthScreen>
