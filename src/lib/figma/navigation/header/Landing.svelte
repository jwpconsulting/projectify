<script lang="ts">
    import { _ } from "svelte-i18n";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import HeaderUniversal from "$lib/figma/navigation/header/HeaderUniversal.svelte";
    import Links from "$lib/figma/navigation/header/Links.svelte";
</script>

<HeaderUniversal logoVisibleDesktop logoVisibleMobile>
    <slot slot="desktop-left">
        <div class="flex flex-row gap-4">
            <Links />
        </div>
    </slot>
    <slot slot="desktop-right">
        <a href="/login">
            <Button
                action={{ kind: "a", href: "/login" }}
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.log-in")}
            />
        </a>
        <a href="/signup">
            <Button
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.start-a-free-trial")}
            />
        </a>
    </slot>
    <div slot="mobile">
        <HamburgerMenu isActive />
    </div>
</HeaderUniversal>
