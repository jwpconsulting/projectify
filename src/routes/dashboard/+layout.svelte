<script lang="ts">
    import AuthGuard from "$lib/components/AuthGuard.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
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
    } from "$lib/stores/globalUi";

    import { user } from "$lib/stores/user";
</script>

<AuthGuard>
    <div class="flex h-screen flex-col">
        {#if $user}
            <HeaderDashboard user={$user} />
        {/if}
        <slot />
    </div>
</AuthGuard>

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
