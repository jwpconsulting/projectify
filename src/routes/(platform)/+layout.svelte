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
        closeMobileMenu,
    } from "$lib/stores/globalUi";
    import { user } from "$lib/stores/user";
</script>

<div class="flex grow flex-col">
    {#if $user}
        <HeaderDashboard user={$user} />
    {/if}
    <div class="relative h-full">
        <OverlayContainer
            closeOverlay={closeMobileMenu}
            fixed={false}
            store={mobileMenuState}
            let:target
        >
            <MobileMenuOverlay {target} />
            <slot slot="else" />
        </OverlayContainer>
    </div>
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
