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

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { requestPasswordResetUrl } from "$lib/urls/user";
</script>

<svelte:head>
    <title>{$_("auth.requested-password-reset.title")}</title>
</svelte:head>

<section class="flex flex-col gap-4 px-8 py-4">
    <h1 class="text-2xl font-bold">
        {$_("auth.requested-password-reset.heading")}
    </h1>
    <p>
        {$_("auth.requested-password-reset.message")}
    </p>
    <p>
        {$_("auth.requested-password-reset.troubleshooting")}
    </p>

    <Anchor
        size="normal"
        label={$_("auth.requested-password-reset.request-again")}
        href={requestPasswordResetUrl}
    />
</section>
