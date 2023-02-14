<script lang="ts">
    import { _ } from "svelte-i18n";
    import Header from "$lib/figma/navigation/header/Header.svelte";
    import HeaderMobile from "$lib/figma/navigation/header/HeaderMobile.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
</script>

<Header logoVisible>
    <slot slot="left">
        <div class="flex flex-row gap-4">
            <Button
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.features")}
            />
            <Button
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.solutions")}
            />
            <Button
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.resources")}
            />
            <Button
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.company")}
            />
            <a href="/signin">
                <Button
                    style={{ kind: "tertiary", icon: null }}
                    color="blue"
                    disabled={false}
                    size="medium"
                    label={$_("header.log-in")}
                />
            </a>
        </div>
    </slot>
    <slot slot="right">
        <a href="/dashboard">
            <Button
                style={{ kind: "primary" }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.continue-to-dashboard")}
            />
        </a>
    </slot>
</Header>

<HeaderMobile logoVisible>
    <HamburgerMenu isActive />
</HeaderMobile>
