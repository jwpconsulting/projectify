<script lang="ts">
    import { user, logout } from "$lib/stores/user";
    import { _ } from "svelte-i18n";
    import DropDownMenu from "./dropDownMenu.svelte";
    import IconLogout from "./icons/icon-logout.svelte";
    import IconUser from "./icons/icon-user.svelte";
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
                    class="overflow-hidden text-ellipsis whitespace-nowrap text-base font-bold normal-case"
                    >{userData.full_name
                        ? userData.full_name
                        : userData.email}</span
                >
            </div>

            <UserProfilePicture
                pictureProps={{
                    url: userData.profile_picture,
                    size: 32,
                }}
            />
        </label>
    </DropDownMenu>
{/if}
