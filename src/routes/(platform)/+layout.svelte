<script lang="ts">
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import {
        mobileMenuState,
        resolveConstructiveOverlay,
        constructiveOverlayState,
        destructiveOverlayState,
        rejectDestructiveOverlay,
        rejectConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import { user } from "$lib/stores/user";
</script>

<div class="flex grow flex-col">
    {#if $user}
        <HeaderDashboard user={$user} />
    {/if}
    {#if $mobileMenuState.kind === "visible"}
        <MobileMenuOverlay target={$mobileMenuState.target} />
    {/if}
    <slot />
</div>

<ConnectionStatus />

<OverlayContainer
    closeOverlay={rejectDestructiveOverlay}
    store={destructiveOverlayState}
    let:target
>
    <DestructiveOverlay {target} />
</OverlayContainer>

<OverlayContainer
    closeOverlay={rejectConstructiveOverlay}
    store={constructiveOverlayState}
    let:target
>
    <ConstructiveOverlay {target} on:cancel={resolveConstructiveOverlay} />
</OverlayContainer>

<ContextMenuContainer />
