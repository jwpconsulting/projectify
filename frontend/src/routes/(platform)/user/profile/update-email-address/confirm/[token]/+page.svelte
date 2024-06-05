<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2024 JWP Consulting GK

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
<!--
    @component Page for user update email token confirmation
-->
<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import {
        confirmedEmailAddressUpdateUrl,
        updateEmailAddressUrl,
    } from "$lib/urls/user";

    import type { PageData } from "./$types";
    import { openApiClient } from "$lib/repository/util";

    export let data: PageData;
    const { token } = data;

    let state:
        | { kind: "submitting" }
        | { kind: "token-error"; message: string }
        | { kind: "error"; message: string } = {
        kind: "submitting",
    };

    onMount(async () => {
        const { error } = await openApiClient.POST(
            "/user/user/email-address-update/confirm",
            { body: { confirmation_token: token } },
        );
        if (error === undefined) {
            await goto(confirmedEmailAddressUpdateUrl);
            return;
        }
        const { details } = error;
        if (details.confirmation_token) {
            state = {
                kind: "token-error",
                message: $_(
                    "user-account-settings.update-email-address.confirm.error.confirmation-token",
                    { values: { error: details.confirmation_token } },
                ),
            };
        } else {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.update-email-address.confirm.error.general",
                ),
            };
        }
    });
</script>

<h1 class="text-center text-2xl font-bold">
    {$_("user-account-settings.update-email-address.confirm.title")}
</h1>
<div class="flex flex-col gap-2">
    {#if state.kind === "submitting"}
        <p>
            {$_(
                "user-account-settings.update-email-address.confirm.submitting",
            )}
        </p>
    {:else}
        <p>
            {state.message}
        </p>
        <h2 class="font-bold">
            {$_(
                "user-account-settings.update-email-address.confirm.error.what-to-do.title",
            )}
        </h2>
        <ul class="list-inside list-disc">
            <li>
                <Anchor
                    label={$_(
                        "user-account-settings.update-email-address.confirm.error.what-to-do.try-again",
                    )}
                    size="normal"
                    href={updateEmailAddressUrl}
                />
            </li>
            <li>
                <Anchor
                    label={$_(
                        "user-account-settings.update-email-address.confirm.error.what-to-do.contact-us.label",
                    )}
                    size="normal"
                    href={$_(
                        "user-account-settings.update-email-address.confirm.error.what-to-do.contact-us.email",
                    )}
                />
            </li>
        </ul>
    {/if}
</div>
