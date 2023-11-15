<script lang="ts">
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import Continue from "$lib/figma/navigation/header/Continue.svelte";
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { closeMobileMenu, mobileMenuState } from "$lib/stores/globalUi";
    import { user } from "$lib/stores/user";
</script>

<div class="flex h-full flex-col bg-background">
    {#if $user}
        <Continue />
    {:else}
        <Landing />
    {/if}
    <div class="relative h-full">
        <OverlayContainer
            closeOverlay={closeMobileMenu}
            fixed={false}
            store={mobileMenuState}
            let:target
        >
            <MobileMenuOverlay slot="default" {target} />
            <div slot="else" class="flex flex-col">
                <slot />
                <Footer />
            </div>
        </OverlayContainer>
    </div>
</div>
