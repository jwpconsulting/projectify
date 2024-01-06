<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Loading from "$lib/components/loading.svelte";
    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import MobileMenu from "$lib/figma/overlays/MobileMenu.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        currentWorkspace,
        currentWorkspaces,
    } from "$lib/stores/dashboard";
    import { closeMobileMenu } from "$lib/stores/globalUi";
    import type { MobileMenuType } from "$lib/types/ui";
    import { dashboardUrl } from "$lib/urls/dashboard";
    import { logInUrl, signUpUrl } from "$lib/urls/user";

    export let target: MobileMenuType;
</script>

<div class="min-h-screen w-full bg-foreground p-2" role="menu">
    <div class="flex h-full flex-col gap-8 p-2">
        {#if target.kind === "dashboard"}
            {#if $currentWorkspaces !== undefined && $currentWorkspace !== undefined}
                <Full
                    workspaces={$currentWorkspaces}
                    workspace={$currentWorkspace}
                />
            {:else}
                <Loading />
            {/if}
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
