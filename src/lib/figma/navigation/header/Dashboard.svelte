<script lang="ts">
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
    import type { User } from "$lib/types/user";

    export let user: User;
</script>

<Layout logoVisibleDesktop>
    <svelte:fragment slot="desktop-right">
        <div class="flex flex-row gap-4">
            <UserAccount {user} />
        </div>
    </svelte:fragment>
    <slot slot="mobile">
        <div class="flex flex-row gap-4">
            <HamburgerMenu
                isActive
                action={() => toggleMobileMenu({ kind: "dashboard" })}
            />
            <SearchMobile />
        </div>

        <div class="flex flex-row gap-4">
            <UserAccount {user} />
        </div>
    </slot>
</Layout>
