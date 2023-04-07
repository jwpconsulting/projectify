<script lang="ts">
    import "../app.scss";
    import "../i18n.js";
    import ConnectionStatus from "$lib/components/connectionStatus.svelte";
    import GlobalDropDown from "$lib/components/globalDropDown.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import {
        closeConstructiveOverlay,
        closeDestructiveOverlay,
        constructiveOverlayState,
        destructiveOverlayState,
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

<OverlayContainer
    overlay={ConstructiveOverlay}
    store={constructiveOverlayState}
    close={closeConstructiveOverlay}
    perform={null}
/>

<ContextMenuContainer />
