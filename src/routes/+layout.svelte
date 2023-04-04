<script lang="ts">
    import "../app.scss";
    import "../i18n.js";
    import ConnectionStatus from "$lib/components/connectionStatus.svelte";
    import GlobalDropDown from "$lib/components/globalDropDown.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import "$lib/stores/global-ui";
    import {
        destructiveOverlayState,
        closeDestructiveOverlay,
        performDestructiveOverlay,
    } from "$lib/stores/global-ui";
</script>

<svelte:head>
    <title>Projectify</title>
    <meta name="description" content="Projects menagemet app" />
</svelte:head>

<slot />

<ConnectionStatus />

<GlobalDropDown />

<OverlayContainer
    overlay={DestructiveOverlay}
    store={destructiveOverlayState}
    close={closeDestructiveOverlay}
    perform={performDestructiveOverlay}
/>
<ContextMenuContainer />
