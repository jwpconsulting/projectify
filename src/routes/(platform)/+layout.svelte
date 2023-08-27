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

<OverlayContainer store={destructiveOverlayState} let:target>
    <DestructiveOverlay
        {target}
        on:cancel={closeDestructiveOverlay}
        on:destroy={performDestructiveOverlay}
    />
</OverlayContainer>

<OverlayContainer store={constructiveOverlayState} let:target>
    <ConstructiveOverlay {target} on:cancel={closeConstructiveOverlay} />
</OverlayContainer>

<ContextMenuContainer />
