<script lang="ts">
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import { Query_WorkspaceTeamMembers } from "$lib/graphql/operations";
    import Loading from "./loading.svelte";
    import UserProfilePicture from "./userProfilePicture.svelte";
    import { createEventDispatcher } from "svelte";

    export let workspaceUUID = null;
    export let selectedUser = null;

    let dispatch = createEventDispatcher();

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

    function selectUser(user) {
        selectedUser = user;
        dispatch("userSelected", { user });
    }
</script>

<div class="w-full bg-base-100 shadow-lg rounded-xl">
    {#if res && $res.loading}
        <div class="w-full h-full flex justify-center items-center py-8">
            <Loading />
        </div>
    {:else}
        <div class="p-4">
            <input
                type="text"
                class="input w-full input-bordered"
                placeholder="Search"
            />
        </div>
        <div class="px-4 font-bold">Team Members</div>
        <ul
            class="menu flex flex-col pb-4 pt-2 divide-y divide-base-300 overflow-y-auto max-h-full"
        >
            {#each users as user}
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
        </ul>
    {/if}
</div>
