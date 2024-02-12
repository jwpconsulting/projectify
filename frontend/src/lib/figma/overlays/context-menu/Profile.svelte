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
    import { Logout, User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { getProfileUrl } from "$lib/urls";
    import { logOutUrl } from "$lib/urls/user";
</script>

<Layout>
    <ContextMenuButton
        kind={{ kind: "a", href: getProfileUrl() }}
        label={$_("overlay.context-menu.profile.my-profile")}
        state="normal"
        icon={User}
    />
    <ContextMenuButton
        kind={{ kind: "a", href: logOutUrl }}
        label={$_("overlay.context-menu.profile.log-out")}
        state="normal"
        icon={Logout}
    />
</Layout>
