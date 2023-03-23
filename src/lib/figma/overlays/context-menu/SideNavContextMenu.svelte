<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getArchiveUrl, getSettingsUrl } from "$lib/urls";
    // TODO we would really like to mock this too and make it injectable
    // for our stories Justus 2023-03-23
    import { sideNavOpen, toggleSideNavOpen } from "$lib/stores/dashboard";
    import {
        ArrowCircleLeft,
        ArrowCircleRight,
        Archive,
        Cog,
    } from "@steeze-ui/heroicons";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
</script>

<ContextMenuButton
    kind={{ kind: "button" }}
    label={$sideNavOpen
        ? $_("side-nav-overlay.minimise-sidebar")
        : $_("side-nav-overlay.expand-sidebar")}
    state="normal"
    on:click={toggleSideNavOpen}
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
