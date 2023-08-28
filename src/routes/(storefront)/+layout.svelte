<script lang="ts">
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import Continue from "$lib/figma/navigation/header/Continue.svelte";
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { mobileMenuState } from "$lib/stores/globalUi";
    import { user } from "$lib/stores/user";
</script>

<div class="flex h-full flex-col bg-background">
    {#if $user}
        <Continue />
    {:else}
        <Landing />
    {/if}
    <div class="relative">
        <slot />
        <OverlayContainer fixed={false} store={mobileMenuState} let:target>
            <MobileMenuOverlay {target} />
        </OverlayContainer>
    </div>
</div>
