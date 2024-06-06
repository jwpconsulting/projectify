<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { logInUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    export let data: PageData;
</script>

<section class="flex flex-col gap-4 px-8 py-4">
    {#if data.error === undefined}
        <h1 class="text-2xl font-bold">
            {$_("auth.confirm-email.success.title")}
        </h1>
        <p>
            {$_("auth.confirm-email.success.message")}
        </p>

        <Anchor
            size="normal"
            label={$_("auth.confirm-email.success.continue")}
            href={logInUrl}
        />
    {:else if data.error.code === 500}
        <p>{$_("auth.confirm-email.error.try-again")}</p>
    {:else if data.error.code === 400}
        <h1 class="text-2xl font-bold">
            {$_("auth.confirm-email.error.title")}
        </h1>
        <p>
            {$_("auth.confirm-email.error.message")}
        </p>
        {#if data.error?.details?.email}
            <p>
                {$_("auth.confirm-email.error.email", {
                    values: { error: data.error.details.email },
                })}
            </p>
        {/if}
        {#if data.error.details.token}
            <p>
                {$_("auth.confirm-email.error.token", {
                    values: { error: data.error.details.token },
                })}
            </p>
        {/if}
        <Anchor
            size="normal"
            label={$_("auth.confirm-email.error.continue")}
            href="/contact-us"
        />
    {/if}
</section>
