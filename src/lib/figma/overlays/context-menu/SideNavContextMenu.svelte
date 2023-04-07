<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getArchiveUrl, getSettingsUrl } from "$lib/urls";
    import {
        Archive,
        ArrowCircleLeft,
        ArrowCircleRight,
        Cog,
    } from "@steeze-ui/heroicons";
    import type { Workspace } from "$lib/types/workspace";
    import type { SideNavModule } from "$lib/types/stores";

    export let sideNavModule: SideNavModule;

    let { sideNavOpen, toggleSideNavOpen } = sideNavModule;

    export let workspace: Workspace;
</script>

<ContextMenuButton
    kind={{ kind: "button", action: toggleSideNavOpen }}
    label={$sideNavOpen
        ? $_("side-nav-overlay.minimise-sidebar")
        : $_("side-nav-overlay.expand-sidebar")}
    state="normal"
    icon={$sideNavOpen ? ArrowCircleLeft : ArrowCircleRight}
/>
<ContextMenuButton
    kind={{ kind: "a", href: getArchiveUrl(workspace.uuid) }}
    label={$_("side-nav-overlay.go-to-archive")}
    state="normal"
    icon={Archive}
/>
<ContextMenuButton
    kind={{ kind: "a", href: getSettingsUrl(workspace.uuid, "index") }}
    label={$_("side-nav-overlay.workspace-settings")}
    state="normal"
    icon={Cog}
/>
