<script lang="ts">
    import { _ } from "svelte-i18n";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Header from "$lib/figma/navigation/header/Header.svelte";
    import HeaderMobile from "$lib/figma/navigation/header/HeaderMobile.svelte";
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
            <a href="/pricing">
                <Button
                    style={{ kind: "tertiary", icon: null }}
                    color="blue"
                    disabled={false}
                    size="medium"
                    label={$_("header.pricing")}
                />
            </a>
        </div>
    </slot>
    <slot slot="right">
        <a href="/signin">
            <Button
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
</Header>

<HeaderMobile logoVisible>
    <div>
        <HamburgerMenu isActive />
    </div>
</HeaderMobile>
