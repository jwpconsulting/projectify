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
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import { startUrl } from "$lib/urls/onboarding";

    import { page } from "$app/stores";
</script>

<Onboarding
    nextLabel={$_("onboarding.error.try-again")}
    nextAction={{ kind: "a", href: startUrl }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.error.title")}</svelte:fragment
    >
    <div class="flex flex-col gap-4" slot="prompt">
        {#if $page.error?.message}
            <h2 class="font-bold">{$_("onboarding.error.error-detail")}</h2>
            <p>{$page.error.message}</p>
        {/if}
        <p>{$_("onboarding.error.message")}</p>
    </div>
    <svelte:fragment slot="content"></svelte:fragment>
</Onboarding>
