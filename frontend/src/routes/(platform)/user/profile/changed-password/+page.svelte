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
    @component Show the user that their password has been changed successfully
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getProfileUrl } from "$lib/urls";
</script>

<h1 class="text-center text-2xl font-bold">
    {$_("user-account-settings.changed-password.title")}
</h1>
<div class="flex flex-col gap-4">
    {$_("user-account-settings.changed-password.message")}
    <Anchor
        label={$_("user-account-settings.changed-password.back-to-profile")}
        href={getProfileUrl()}
        size="normal"
    />
</div>
