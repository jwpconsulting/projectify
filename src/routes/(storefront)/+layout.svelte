<script lang="ts">
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import Continue from "$lib/figma/navigation/header/Continue.svelte";
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { mobileMenuState } from "$lib/stores/globalUi";
    import { user } from "$lib/stores/user";
</script>

<div class="flex h-full grow flex-col bg-foreground">
    {#if $user}
        <Continue />
    {:else}
        <Landing />
    {/if}
    <div class="relative flex h-full grow flex-col">
        {#if $mobileMenuState.kind === "visible"}
            <div class="w-full border-b-2 border-border md:hidden">
                <MobileMenuOverlay target={$mobileMenuState.target} />
            </div>
        {/if}
        <div class="flex grow flex-col justify-between">
            <main class="flex grow flex-col">
                <slot />
            </main>
            <Footer />
        </div>
    </div>
</div>
