<script lang="ts">
    import { user, logout } from "$lib/stores/user";
    import { _ } from "svelte-i18n";
    import DropDownMenu from "./dropDownMenu.svelte";
    import IconLogout from "./icons/icon-logout.svelte";
    import IconUser from "./icons/icon-user.svelte";

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
                    >{userData?.email}</span
                >
            </div>
            <div
                class="m-1 flex -space-x-1 overflow-hidden w-8 h-8 rounded-full shrink-0 ring-2"
            >
                <img
                    draggable="false"
                    width="100%"
                    height="100%"
                    src="https://picsum.photos/200"
                    alt="user"
                />
            </div>
        </label>
    </DropDownMenu>
{/if}
