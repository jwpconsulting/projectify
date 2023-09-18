<script lang="ts">
    import { _ } from "svelte-i18n";

    import SideNav from "../navigation/SideNav.svelte";

    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        currentWorkspace,
        currentWorkspaces,
    } from "$lib/stores/dashboard";
    import { closeMobileMenu } from "$lib/stores/globalUi";
    import type { MobileMenuType } from "$lib/types/ui";

    export let target: MobileMenuType;
</script>

<div class="h-full w-full bg-foreground px-2 py-4" role="menu">
    <div class="flex flex-col gap-8 p-4">
        {#if target.kind === "dashboard" && $currentWorkspaces !== undefined}
            <SideNav
                workspaces={$currentWorkspaces}
                workspace={$currentWorkspace}
            />
        {:else}
            <MobileMenu />
        {/if}
        {#if target.kind === "continue"}
            <Button
                action={{
                    kind: "a",
                    href: "/dashboard",
                    onInteract: () => {
                        closeMobileMenu();
                        console.log("closing");
                    },
                }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label={$_("header.continue-to-dashboard")}
            />
        {:else if target.kind === "landing"}
            <Button
                action={{
                    kind: "a",
                    href: "/login",
                    onInteract: closeMobileMenu,
                }}
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                size="medium"
                label={$_("header.log-in")}
            />
            <Button
                action={{
                    kind: "a",
                    href: "/signup",
                    onInteract: closeMobileMenu,
                }}
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label={$_("header.start-a-free-trial")}
            />
        {/if}
    </div>
</div>
