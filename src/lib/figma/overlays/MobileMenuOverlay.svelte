<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { escape, closeMobileMenu } from "$lib/stores/globalUi";
    import type { MobileMenuType } from "$lib/types/ui";

    export let target: MobileMenuType;
    onMount(() => {
        console.log("TODO", target);
    });
    $: {
        if ($escape) {
            closeMobileMenu();
        }
    }
</script>

<div class="h-full w-full bg-foreground px-2 py-4" role="menu">
    <HamburgerMenu action={closeMobileMenu} isActive />
    <MobileMenu />
    <div class="px-4">
        <Button
            action={{ kind: "a", href: "/dashboard" }}
            style={{ kind: "primary" }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.continue-to-dashboard")}
        />
    </div>
</div>
