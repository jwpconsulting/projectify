<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
