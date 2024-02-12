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

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
</script>

<Layout>
    <!-- TODO simplify and add some kind of call back -->
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("all roles not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.all-roles")}
        state="normal"
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("owner not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.owner")}
        state="normal"
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("maintainer not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.maintainer")}
        state="normal"
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("member not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.member")}
        state="normal"
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("observer not implemented"),
        }}
        label={$_("overlay.context-menu.permissions.observer")}
        state="normal"
    />
</Layout>
