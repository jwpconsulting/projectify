<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import {
        confirmedEmailAddressUpdateUrl,
        getLogInWithNextUrl,
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
        if (error.code === 403) {
            await goto(getLogInWithNextUrl(window.location.href));
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_(
                    "user-account-settings.update-email-address.confirm.error.general",
                ),
            };
            return;
        }
        const { details } = error;
        state = {
            kind: "token-error",
            message: $_(
                "user-account-settings.update-email-address.confirm.error.confirmation-token",
                { values: { error: details.confirmation_token } },
            ),
        };
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
