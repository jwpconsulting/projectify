<script lang="ts">
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import { getWorkspace } from "$lib/repository";
    import Loading from "./loading.svelte";
    import UserProfilePicture from "./userProfilePicture.svelte";
    import { createEventDispatcher, onMount } from "svelte";
    import { user } from "$lib/stores/user";

    import Fuse from "fuse.js";
    import SearchInput from "./search-input.svelte";
    import { fuseSearchThreshold } from "$lib/stores/dashboard";

    export let workspaceUUID = null;
    export let selectedUser = null;
    export let enableUnassignedSelection = false;

    export let dispatch = createEventDispatcher();

    let res = null;
    let loading = true;
    let workspaceWSStore;
    let workspace = null;
    let users = [];

    async function fetch() {
        res = await getWorkspace(workspaceUUID);
        loading = false;
    }

    const refetch = debounce(() => {
        fetch();
    }, 100);

    $: {
        if (workspaceUUID) {
            fetch();

            workspaceWSStore = getSubscriptionForCollection(
                "workspace",
                workspaceUUID
            );
        }
    }

    $: {
        if ($workspaceWSStore) {
            refetch();
        }
    }

    $: {
        if (res) {
            workspace = res;
            if (workspace["workspace_users"]) {
                users = workspace["workspace_users"];
            }
        }
    }

    let searchText = "";
    let searchEngine = null;
    let filteredUsers = [];
    $: {
        searchEngine = new Fuse(users, {
            keys: ["user.email", "user.full_name"],
            threshold: fuseSearchThreshold,
        });
    }

    $: {
        if (searchText.length) {
            filteredUsers = searchEngine
                .search(searchText)
                .map((res) => res.item);
        } else {
            filteredUsers = users;
        }
    }

    function selectUser(user) {
        selectedUser = user;
        dispatch("userSelected", { user });
    }

    let searchFieldEl;
    $: {
        if (searchFieldEl) {
            searchFieldEl.focus();
        }
    }

    function selectMe() {
        // find self in users
        const self = users.find((el) => el.user.email == $user.email);
        selectUser(self);
    }

    function clearSelection() {
        selectUser(null);
    }

    function onBlur(event) {
        if (!event.currentTarget.contains(event.relatedTarget)) {
            dispatch("blur");
        }
    }

    let rootEl;
</script>

<div
    class="w-full overflow-hidden rounded-xl bg-base-100 shadow-lg"
    tabindex="-1"
    bind:this={rootEl}
    on:blur={onBlur}
>
    {#if loading}
        <div class="flex h-full w-full items-center justify-center py-8">
            <Loading />
        </div>
    {:else}
        <div class="p-4">
            <SearchInput
                placeholder={$_("search-team-member")}
                bind:inputElement={searchFieldEl}
                bind:searchText
                on:blur={() => rootEl.focus()}
            />
        </div>
        <div class="px-4 font-bold">Team Members</div>
        <ul
            class="menu flex max-h-full flex-col divide-y divide-base-300 overflow-y-auto pt-2"
        >
            {#each filteredUsers as user}
                <li>
                    <a
                        class:active={selectedUser &&
                            selectedUser.email == user.user.email}
                        class="flex flex-row space-x-4"
                        href="/"
                        on:click|preventDefault={(e) => {
                            selectUser(user);
                        }}
                    >
                        <UserProfilePicture
                            pictureProps={{
                                url: user.user.profile_picture,
                                size: 42,
                            }}
                        />

                        <div class="flex grow flex-col justify-start">
                            <div class="text-xs">Interface designer</div>
                            <div class="font-bold">
                                {user.user.full_name
                                    ? user.user.full_name
                                    : user.user.email}
                            </div>
                        </div>
                    </a>
                </li>
            {/each}

            {#if enableUnassignedSelection}
                <li>
                    <a
                        class:active={selectedUser == "unassigned"}
                        class="flex flex-row space-x-4"
                        href="/"
                        on:click|preventDefault={(e) => {
                            selectUser("unassigned");
                        }}
                    >
                        <div
                            class="flex grow flex-col items-center justify-center"
                        >
                            <div class="font-bold">
                                {$_("assigned-to-nobody")}
                            </div>
                        </div>
                    </a>
                </li>
            {/if}
        </ul>
        <footer
            class="min-h-8 flex divide-x divide-base-300 border-t border-base-300"
        >
            {#if selectedUser}
                <div
                    class="footer-btn flex h-8 grow items-center justify-center text-primary"
                    on:click={clearSelection}
                >
                    <div class="text-xs ">{$_("clear-selection")}</div>
                </div>
            {/if}
            {#if selectedUser?.email !== $user?.email}
                <div
                    class="footer-btn flex h-8 grow items-center justify-center text-primary"
                    on:click={selectMe}
                >
                    <div class="text-xs ">{$_("select-me")}</div>
                </div>
            {/if}
        </footer>
    {/if}
</div>

<style lang="scss">
    .footer-btn {
        @apply cursor-pointer;
        > * {
            @apply transition-all;
        }
        &:hover {
            @apply bg-base-200;
        }

        &.active {
            @apply bg-primary text-primary-content shadow-md;
        }
    }
</style>
