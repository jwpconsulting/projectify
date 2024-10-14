<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { closeMobileMenu } from "$lib/stores/globalUi";
    import type { MobileMenuType } from "$lib/types/ui";
    import { dashboardUrl } from "$lib/urls/dashboard";
    import { logInUrl, signUpUrl } from "$lib/urls/user";

    export let target: MobileMenuType;
    export let minHScreen = true;
</script>

<div
    class="w-full bg-foreground p-2"
    class:min-h-screen={minHScreen}
    role="menu"
>
    <div class="flex h-full flex-col gap-4 p-2">
        {#if target.kind === "dashboard"}
            <Full />
        {:else}
            <MobileMenu />
        {/if}
        {#if target.kind === "continue"}
            <Button
                action={{
                    kind: "a",
                    href: dashboardUrl,
                    onInteract: () => {
                        closeMobileMenu();
                        console.log("closing");
                    },
                }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label={$_("navigation.header.continue-to-dashboard")}
            />
        {:else if target.kind === "landing"}
            <Button
                action={{
                    kind: "a",
                    href: logInUrl,
                    onInteract: closeMobileMenu,
                }}
                style={{ kind: "tertiary" }}
                color="blue"
                size="medium"
                label={$_("navigation.header.log-in")}
            />
            <Button
                action={{
                    kind: "a",
                    href: signUpUrl,
                    onInteract: closeMobileMenu,
                }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label={$_("navigation.header.start-a-free-trial")}
            />
        {/if}
    </div>
</div>
