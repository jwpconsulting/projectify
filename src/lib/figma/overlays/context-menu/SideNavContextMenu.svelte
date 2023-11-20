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
