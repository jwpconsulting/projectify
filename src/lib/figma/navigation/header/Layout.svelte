<script lang="ts">
    import { _ } from "svelte-i18n";

    import PolyLogo from "$lib/figma/navigation/polylogo.svg";

    export let logoVisibleDesktop = false;
    export let logoVisibleMobile = false;
    export let alwaysVisible = false;

    $: justCenter =
        !$$slots["desktop-left"] &&
        !$$slots["desktop-right"] &&
        $$slots["desktop-center"];
    // There are lots of conditionals here, it might make sense to refactor
    // it a bit
</script>

<nav
    class="hidden flex-row items-center justify-between border-b-2 border-border bg-foreground px-6 py-4 md:flex"
    class:justify-between={!justCenter}
    class:justify-center={justCenter}
    class:hidden={!alwaysVisible}
    class:flex={alwaysVisible}
>
    <div class="flex flex-row items-center gap-4">
        {#if logoVisibleDesktop}
            <a href="/" class="shrink">
                <img src={PolyLogo} alt={$_("navigation.header.logo.alt")} />
            </a>
        {/if}
        {#if $$slots["desktop-left"]}
            <div class="flex flex-row gap-2">
                <slot name="desktop-left" />
            </div>
        {/if}
    </div>
    <slot name="desktop-center" />
    {#if $$slots["desktop-right"]}
        <div class="flex shrink-0 flex-row items-center gap-2">
            <slot name="desktop-right" />
        </div>
    {/if}
</nav>

{#if !alwaysVisible}
    <nav
        class="flex flex-row items-center justify-between border-b-2 border-border bg-foreground px-2 py-4 md:hidden"
    >
        {#if logoVisibleMobile}
            <a href="/">
                <img src={PolyLogo} alt={$_("navigation.header.logo.alt")} />
                <!-- TODO add text that says "back to landing" for AT users -->
            </a>
        {/if}
        <slot name="mobile" />
    </nav>
{/if}
