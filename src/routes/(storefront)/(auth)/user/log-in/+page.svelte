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
    import { login } from "$lib/stores/user";
    import type { AuthViewState } from "$lib/types/ui";
    import { signUpUrl, requestPasswordResetUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { redirectTo } = data;

    let email: string | undefined = undefined;
    let password: string | undefined = undefined;

    let state: AuthViewState = { kind: "start" };

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
        try {
            await login(email, password, redirectTo, { fetch });
        } catch {
            // TODO set the error to something meaningful
            state = {
                kind: "error",
                message: $_("auth.log-in.invalid-credentials"),
            };
        }
    }
</script>

<AuthScreen title={$_("auth.log-in.title")} {action}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.log-in.email.placeholder")}
            style={{ inputType: "email" }}
            name="email"
            label={$_("auth.log-in.email.label")}
            required
            bind:value={email}
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
            label={$_("auth.log-in.log-in")}
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
