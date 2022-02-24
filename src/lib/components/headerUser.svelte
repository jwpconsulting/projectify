<script lang="ts">
    import { user, logout } from "$lib/stores/user";
    import { _ } from "svelte-i18n";
    import DropDownMenu from "./dropDownMenu.svelte";
    import IconLogout from "./icons/icon-logout.svelte";
    import IconUser from "./icons/icon-user.svelte";
    import vars from "$lib/env";
    import UserProfilePicture from "./userProfilePicture.svelte";
    $: userData = $user;
</script>

{#if userData}
    <DropDownMenu
        items={[
            {
                label: $_("my-profile"),
                icon: IconUser,
                href: "/user/profile",
            },
            {
                label: $_("logout"),
                icon: IconLogout,
                onClick: () => {
                    logout();
                },
            },
        ]}
    >
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label tabindex="0" class="btn btn-ghost space-x-2">
            <div class="flex">
                <span
                    class="text-base font-bold normal-case overflow-hidden whitespace-nowrap text-ellipsis"
                    >{userData.fullName
                        ? userData.fullName
                        : userData.email}</span
                >
            </div>
            <UserProfilePicture size={32} url={userData.profilePicture} />
        </label>
    </DropDownMenu>
{/if}
