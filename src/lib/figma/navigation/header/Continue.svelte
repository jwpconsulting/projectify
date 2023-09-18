<script lang="ts">
    import { _ } from "svelte-i18n";

    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import Links from "$lib/figma/navigation/header/Links.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
</script>

<Layout logoVisibleDesktop logoVisibleMobile>
    <svelte:fragment slot="desktop-left">
        <Links />
    </svelte:fragment>
    <slot slot="desktop-right">
        <Button
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("header.continue-to-dashboard")}
            action={{ kind: "a", href: "/dashboard" }}
        />
    </slot>
    <HamburgerMenu
        slot="mobile"
        isActive
        action={() => toggleMobileMenu({ kind: "continue" })}
    />
</Layout>
