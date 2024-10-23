<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
    import { sideNavOpen, toggleSideNavOpen } from "$lib/stores/dashboard/ui";
    import type { WorkspaceDetail } from "$lib/types/workspace";
    import { getArchiveUrl, getSettingsUrl } from "$lib/urls";

    export let workspace: Pick<WorkspaceDetail, "uuid">;
</script>

<Layout>
    <ContextMenuButton
        kind={{ kind: "button", action: toggleSideNavOpen }}
        label={$sideNavOpen
            ? $_("overlay.context-menu.side-nav.minimise-sidebar")
            : $_("overlay.context-menu.side-nav.expand-sidebar")}
        icon={$sideNavOpen ? ArrowCircleLeft : ArrowCircleRight}
    />
    <ContextMenuButton
        kind={{ kind: "a", href: getArchiveUrl(workspace) }}
        label={$_("overlay.context-menu.side-nav.go-to-archive")}
        icon={Archive}
    />
    <ContextMenuButton
        kind={{ kind: "a", href: getSettingsUrl(workspace, "index") }}
        label={$_("overlay.context-menu.side-nav.workspace-settings")}
        icon={Cog}
    />
</Layout>
