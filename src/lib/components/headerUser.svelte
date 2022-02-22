<script lang="ts">
    import { user, logout } from "$lib/stores/user";
    import { _ } from "svelte-i18n";
    import IconLogout from "./icons/icon-logout.svelte";

    $: userData = $user;
</script>

{#if userData}
    <!-- <button
        class="flex p-3 justify-center items-center hover:bg-base-200 h-14 rounded"
    >
        <div class="flex mr-2   ">
            <span
                class="text-base font-bold overflow-hidden whitespace-nowrap text-ellipsis"
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
    </button> -->

    <div class="dropdown dropdown-end">
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
        <ul
            tabindex="0"
            class="menu dropdown-content bg-base-100 rounded-box min-w-[200px] shadow-xl"
        >
            <li>
                <a
                    class="space-x-2 text-error"
                    href="/"
                    on:click|preventDefault={() => logout()}
                >
                    <IconLogout /><span>{$_("logout")}</span>
                </a>
            </li>
        </ul>
    </div>
{/if}
