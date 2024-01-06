<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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

    import HeaderButton from "$lib/funabashi/buttons/HeaderButton.svelte";
    import { closeMobileMenu } from "$lib/stores/globalUi";

    $: links = [
        { label: $_("navigation.header.solutions"), href: "/solutions" },
        { label: $_("navigation.header.help"), href: "/help" },
        { label: $_("navigation.header.pricing"), href: "/pricing" },
    ];
</script>

<div class="flex flex-col gap-4 divide-y divide-border">
    {#each links as link}
        <HeaderButton
            action={{
                kind: "a",
                href: link.href,
                onInteract: closeMobileMenu,
            }}
            label={link.label}
        />
    {/each}
</div>
