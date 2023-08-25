<script lang="ts">
    import ConnectionStatus from "$lib/components/connectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import {
        closeConstructiveOverlay,
        closeDestructiveOverlay,
        constructiveOverlayState,
        destructiveOverlayState,
        performDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import { user } from "$lib/stores/user";
</script>

<div class="flex h-full flex-col">
    {#if $user}
        <HeaderDashboard user={$user} />
    {/if}
    <slot />
</div>

<ConnectionStatus />

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
