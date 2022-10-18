<script lang="ts">
    import { _ } from "svelte-i18n";
    import MenuButton from "$lib/figma/buttons/MenuButton.svelte";
    import { getArchiveUrl, getSettingsUrl } from "$lib/urls";
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

<MenuButton
    kind={{ kind: "button" }}
    label={$sideNavOpen
        ? $_("side-nav-overlay.minimise-sidebar")
        : $_("side-nav-overlay.expand-sidebar")}
    state="normal"
    on:click={toggleSideNavOpen}
    icon={$sideNavOpen ? ArrowCircleLeft : ArrowCircleRight}
/>
<MenuButton
    kind={{ kind: "a", href: getArchiveUrl(workspace.uuid) }}
    label={$_("side-nav-overlay.go-to-archive")}
    state="normal"
    icon={Archive}
/>
<MenuButton
    kind={{ kind: "a", href: getSettingsUrl(workspace.uuid, "index") }}
    label={$_("side-nav-overlay.workspace-settings")}
    state="normal"
    icon={Cog}
/>
