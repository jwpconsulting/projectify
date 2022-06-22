<script lang="ts">
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import { Query_WorkspaceTeamMembers } from "$lib/graphql/operations";
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
    let workspaceWSStore;
    let workspace = null;
    let users = [];

    const refetch = debounce(() => {
        res.refetch();
    }, 100);

    $: {
        if (workspaceUUID) {
            res = query(Query_WorkspaceTeamMembers, {
                variables: { uuid: workspaceUUID },
                fetchPolicy: "network-only",
            });

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
        if (res && $res.data) {
            workspace = $res.data["workspace"];
            if (workspace["users"]) {
                users = workspace["users"];
            }
        }
    }

    let searchText = "";
    let searchEngine = null;
    let filteredUsers = [];
    $: {
        searchEngine = new Fuse(users, {
            keys: ["email", "fullName"],
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

    let serachFieldEl;
    $: {
        if (serachFieldEl) {
            serachFieldEl.focus();
        }
    }

    function selectMe() {
        selectUser($user);
    }

    function clearSelection() {
        selectUser(null);
    }
</script>

<div class="w-full overflow-hidden rounded-xl bg-base-100 shadow-lg">
    {#if res && $res.loading}
        <div class="flex h-full w-full items-center justify-center py-8">
            <Loading />
        </div>
    {:else}
        <div class="p-4">
            <SearchInput
                placeholder={$_("search-team-member")}
                bind:inputElement={serachFieldEl}
                bind:searchText
            />
        </div>
        <div class="px-4 font-bold">Team Members</div>
        <ul
            class="menu flex flex-col pt-2 divide-y divide-base-300 overflow-y-auto max-h-full"
        >
            {#each filteredUsers as user}
                <li>
                    <a
                        class:active={selectedUser &&
                            selectedUser.email == user.email}
                        class="flex flex-row space-x-4"
                        href="/"
                        on:click|preventDefault={(e) => {
                            selectUser(user);
                        }}
                    >
                        <UserProfilePicture
                            pictureProps={{
                                url: user.profilePicture,
                                size: 42,
                            }}
                        />

                        <div class="grow flex flex-col justify-start">
                            <div class="text-xs">Interface designer</div>
                            <div class="font-bold">
                                {user.fullName ? user.fullName : user.email}
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
                            class="grow flex flex-col justify-center items-center"
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
            class="flex divide-x divide-base-300 border-t border-base-300 min-h-8"
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
