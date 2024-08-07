<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import {
        mobileMenuState,
        resolveConstructiveOverlay,
        constructiveOverlayState,
        destructiveOverlayState,
        rejectDestructiveOverlay,
        rejectConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import { currentUser } from "$lib/stores/user";
</script>

<!--
With no overflow, we needed to change h-screen -> min-h-screen,
otherwise the footer will be placed inside the dashboard.
TODO evaluate whether grow is still necessary. Seems that with grow set, we wouldn't need min-h-screen, really.
-->
<div class="flex min-h-screen grow flex-col">
    <HeaderDashboard user={$currentUser} />
    {#if $mobileMenuState.kind === "visible"}
        <MobileMenuOverlay target={$mobileMenuState.target} />
    {/if}
    <div class="flex min-h-0 shrink grow flex-row">
        <!-- this breakpoint is in tune with the mobile menu breakpoint -->
        <div class="hidden h-full shrink-0 md:block">
            <SideNav />
        </div>
        <!-- not inserting min-w-0 will mean that this div will extend as much as
    needed around whatever is inside the slot -->
        <div class="min-w-0 grow">
            <slot />
        </div>
    </div>
</div>

<ConnectionStatus />

<OverlayContainer
    closeOverlay={rejectDestructiveOverlay}
    store={destructiveOverlayState}
    let:target
>
    <DestructiveOverlay {target} />
</OverlayContainer>

<OverlayContainer
    closeOverlay={rejectConstructiveOverlay}
    store={constructiveOverlayState}
    let:target
>
    <ConstructiveOverlay {target} on:cancel={resolveConstructiveOverlay} />
</OverlayContainer>

<ContextMenuContainer />
