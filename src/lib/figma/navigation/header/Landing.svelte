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
            action={{ kind: "a", href: "/login" }}
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            size="medium"
            label={$_("header.log-in")}
        />
        <Button
            action={{ kind: "a", href: "/signup" }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("header.start-a-free-trial")}
        />
    </slot>
    <div slot="mobile">
        <HamburgerMenu
            action={() => toggleMobileMenu({ kind: "landing" })}
            isActive
        />
    </div>
</Layout>
