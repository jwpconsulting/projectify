<script lang="ts">
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import SearchButton from "$lib/figma/buttons/SearchButton.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import HeaderUniversal from "$lib/figma/navigation/header/HeaderUniversal.svelte";
    import { openMobileMenu } from "$lib/stores/globalUi";
    import type { User } from "$lib/types/user";

    export let user: User;

    const showSearch = false;
    const showNotificationButton = false;
</script>

<HeaderUniversal logoVisibleDesktop>
    <slot slot="desktop-right">
        {#if showSearch}
            <SearchButton />
        {/if}
        <div class="flex flex-row gap-4">
            {#if showNotificationButton}
                <NotificationButton isActive />
            {/if}
            <UserAccount {user} />
        </div>
    </slot>
    <slot slot="mobile">
        <div class="flex flex-row gap-4">
            <HamburgerMenu
                isActive
                action={() => openMobileMenu({ kind: "dashboard" })}
            />
            {#if showSearch}
                <SearchMobile />
            {/if}
        </div>

        <div class="flex flex-row gap-4">
            {#if showNotificationButton}
                <NotificationButton isActive />
            {/if}
            <UserAccount {user} />
        </div>
    </slot>
</HeaderUniversal>
