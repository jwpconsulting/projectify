<script lang="ts">
    import { _ } from "svelte-i18n";
    import HeaderUniversal from "$lib/figma/navigation/header/HeaderUniversal.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import Links from "$lib/figma/navigation/header/Links.svelte";
</script>

<HeaderUniversal logoVisibleDesktop logoVisibleMobile>
    <slot slot="desktop-left">
        <div class="flex flex-row gap-4"><Links /></div>
    </slot>
    <slot slot="desktop-right">
        <Button
            style={{ kind: "primary" }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.continue-to-dashboard")}
            action={{ kind: "a", href: "/dashboard" }}
        />
    </slot>
    <HamburgerMenu slot="mobile" isActive />
</HeaderUniversal>
