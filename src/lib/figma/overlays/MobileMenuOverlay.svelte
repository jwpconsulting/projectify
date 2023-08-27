<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { closeMobileMenu, handleEscape } from "$lib/stores/globalUi";
    import type { MobileMenuType } from "$lib/types/ui";

    export let target: MobileMenuType;
    onMount(() => {
        console.log("TODO", target);
        return handleEscape(closeMobileMenu);
    });
</script>

<div class="h-full w-full bg-foreground px-2 py-4" role="menu">
    <HamburgerMenu action={closeMobileMenu} isActive />
    <div class="flex flex-col gap-8 p-4">
        <MobileMenu />
        {#if target.kind === "continue"}
            <Button
                action={{ kind: "a", href: "/dashboard" }}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.continue-to-dashboard")}
            />
        {:else if target.kind === "landing"}
            <Button
                action={{ kind: "a", href: "/login" }}
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.log-in")}
            />
            <Button
                action={{ kind: "a", href: "/signup" }}
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.start-a-free-trial")}
            />
        {/if}
    </div>
</div>
