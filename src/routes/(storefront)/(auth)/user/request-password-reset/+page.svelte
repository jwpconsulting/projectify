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
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { requestPasswordReset } from "$lib/repository/user";

    let email: string;

    async function submit() {
        // TODO do some kind of validation here
        await requestPasswordReset(email, { fetch });
        // TODO redirect when successful
    }
</script>

<AuthScreen title={$_("auth.request-password-reset.title")} action={submit}>
    <div class="text-center">
        {$_("auth.request-password-reset.explanation")}
    </div>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.request-password-reset.enter-your-email")}
            style={{ inputType: "email" }}
            name="email"
            label={$_("auth.request-password-reset.email")}
            bind:value={email}
            required
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("auth.request-password-reset.send-reset-password-link")}
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
