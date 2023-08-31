<script lang="ts">
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        closeMobileMenu,
        mobileMenuState,
        toggleMobileMenu,
    } from "$lib/stores/globalUi";
    import type { MobileMenuType } from "$lib/types/ui";

    export let mobileMenuType: MobileMenuType;

    let status = "none";

    async function toggleMenu() {
        status = "Toggling";
        await toggleMobileMenu(mobileMenuType);
        status = "Toggling done";
    }

    function closeMenu() {
        status = "Closing mobile menu";
        closeMobileMenu();
        status = "Closed mobile menu";
    }
</script>

<div class="flex h-full flex-col">
    <p>
        Status: {status}
    </p>
    <div class="flex flex-row">
        <Button
            action={{
                kind: "button",
                action: toggleMenu,
            }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label="Toggle mobile menu"
        />
        <Button
            action={{
                kind: "button",
                action: closeMenu,
            }}
            style={{ kind: "secondary" }}
            color="blue"
            size="medium"
            label="Close mobile menu"
        />
    </div>
    <div class="relative grow">
        <OverlayContainer fixed={false} store={mobileMenuState} let:target>
            <MobileMenuOverlay slot="default" {target} />
            <p slot="else">
                MobileMenuOverlay comes here, but it is not visible right now
            </p>
        </OverlayContainer>
    </div>
</div>
