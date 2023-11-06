<script lang="ts">
    import { _ } from "svelte-i18n";
    import HamburgerMenu from "$lib/figma/buttons/HamburgerMenu.svelte";
    import NotificationButton from "$lib/figma/buttons/NotificationButton.svelte";
    import SearchMobile from "$lib/figma/buttons/SearchMobile.svelte";
    import UserAccount from "$lib/figma/buttons/UserAccount.svelte";
    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { toggleMobileMenu } from "$lib/stores/globalUi";
    import type { User } from "$lib/types/user";
    import { taskSearchInput } from "$lib/stores/dashboard/task";

    export let user: User;

    const showNotificationButton = false;
</script>

<Layout logoVisibleDesktop>
    <slot slot="desktop-right">
        <InputField
            style={{ kind: "search" }}
            placeholder={$_("dashboard.search-task")}
            name="search"
            bind:value={$taskSearchInput}
        />
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
                action={() => toggleMobileMenu({ kind: "dashboard" })}
            />
            <SearchMobile />
        </div>

        <div class="flex flex-row gap-4">
            {#if showNotificationButton}
                <NotificationButton isActive />
            {/if}
            <UserAccount {user} />
        </div>
    </slot>
</Layout>
