<script lang="ts">
    import { _ } from "svelte-i18n";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import HeaderMobile from "$lib/figma/navigation/header/HeaderMobile.svelte";
</script>

<div
    class="hidden flex-row items-center justify-between border-b-2 border-border bg-foreground
    py-4 px-6 lg:flex"
>
    <div class="flex flex-row items-center gap-12">
        <a href="/">
            <img src="/assets/logo/polylogo.svg" alt="" />
        </a>
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
    </div>

    <div class="flex flex-row gap-6">
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
    </div>
</div>

<HeaderMobile logoVisible>
    <div>
        <HamburgerMenu isActive />
    </div>
</HeaderMobile>
