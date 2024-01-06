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
    // TODO rename to just context-menu/ContextMenu
    import {
        Archive,
        ArrowCircleLeft,
        ArrowCircleRight,
        Cog,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { sideNavOpen, toggleSideNavOpen } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";
    import { getArchiveUrl, getSettingsUrl } from "$lib/urls";

    export let workspace: Workspace;
</script>

<Layout>
    <ContextMenuButton
        kind={{ kind: "button", action: toggleSideNavOpen }}
        label={$sideNavOpen
            ? $_("overlay.context-menu.side-nav.minimise-sidebar")
            : $_("overlay.context-menu.side-nav.expand-sidebar")}
        state="normal"
        icon={$sideNavOpen ? ArrowCircleLeft : ArrowCircleRight}
    />
    <ContextMenuButton
        kind={{ kind: "a", href: getArchiveUrl(workspace.uuid) }}
        label={$_("overlay.context-menu.side-nav.go-to-archive")}
        state="normal"
        icon={Archive}
    />
    <ContextMenuButton
        kind={{ kind: "a", href: getSettingsUrl(workspace.uuid, "index") }}
        label={$_("overlay.context-menu.side-nav.workspace-settings")}
        state="normal"
        icon={Cog}
    />
</Layout>
