<script lang="ts">
    import HeaderUniversal from "$lib/figma/navigation/header/HeaderUniversal.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import SearchButton from "$lib/figma/buttons/SearchButton.svelte";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
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
            <HamburgerMenu isActive />
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
