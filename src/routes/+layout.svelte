<script lang="ts">
    import "../app.scss";
    import "../i18n.js";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { mobileMenuState } from "$lib/stores/globalUi";
</script>

<svelte:head>
    <title>Projectify</title>
    <meta
        name="description"
        content="Projectify - Manage projects the right way"
    />
</svelte:head>

<slot />

<OverlayContainer store={mobileMenuState} let:target>
    <MobileMenuOverlay {target} />
</OverlayContainer>
