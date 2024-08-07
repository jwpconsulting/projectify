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
    import Loading from "$lib/components/Loading.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
    import type { CurrentUser } from "$lib/types/user";
    import { dashboardUrl } from "$lib/urls/dashboard";

    export let user: CurrentUser;
</script>

<Layout logoVisibleDesktop logoHref={dashboardUrl}>
    <svelte:fragment slot="desktop-right">
        <div class="flex flex-row gap-4">
            {#if user.kind === "authenticated"}
                <UserAccount {user} />
            {:else}
                <Loading size={5} />
            {/if}
        </div>
    </svelte:fragment>
    <slot slot="mobile">
        <HamburgerMenu
            isActive
            action={() => toggleMobileMenu({ kind: "dashboard" })}
        />

        <div class="flex flex-row gap-4">
            {#if user.kind === "authenticated"}
                <UserAccount {user} />
            {/if}
        </div>
    </slot>
</Layout>
