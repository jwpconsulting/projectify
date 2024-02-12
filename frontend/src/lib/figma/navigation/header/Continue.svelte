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

    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import Links from "$lib/figma/navigation/header/Links.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
</script>

<Layout logoVisibleDesktop logoVisibleMobile>
    <svelte:fragment slot="desktop-left">
        <Links />
    </svelte:fragment>
    <slot slot="desktop-right">
        <Button
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("navigation.header.continue-to-dashboard")}
            action={{ kind: "a", href: "/dashboard" }}
        />
    </slot>
    <HamburgerMenu
        slot="mobile"
        isActive
        action={() => toggleMobileMenu({ kind: "continue" })}
    />
</Layout>
