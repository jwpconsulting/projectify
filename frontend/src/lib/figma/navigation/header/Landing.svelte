<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
            action={{ kind: "a", href: "/user/log-in" }}
            style={{ kind: "tertiary" }}
            color="blue"
            size="medium"
            label={$_("navigation.header.log-in")}
        />
        <Button
            action={{ kind: "a", href: "/user/sign-up" }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("navigation.header.start-a-free-trial")}
        />
    </slot>
    <div slot="mobile">
        <HamburgerMenu
            action={() => toggleMobileMenu({ kind: "landing" })}
            isActive
        />
    </div>
</Layout>
