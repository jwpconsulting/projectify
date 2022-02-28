<script lang="ts">
    import { Query_WorkspaceTeamMembers } from "$lib/graphql/operations";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import Loading from "../loading.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    export let workspaceUUID = null;

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

    function onNewMember() {
        console.log("onNewMember");
    }
</script>

{#if $res.loading}
    <div class="flex items-center justify-center min-h-[200px]">
        <Loading />
    </div>
{:else}
    <div class=" divide-y divide-base-300">
        {#each users as user}
            <div class="flex px-4 py-4 space-x-4">
                <UserProfilePicture url={user.profilePicture} size={42} />
                <div class="grow flex flex-col  justify-center">
                    <div class="text-xs">Interface designer</div>
                    <div class="font-bold">
                        {user.fullName ? user.fullName : user.email}
                    </div>
                </div>
                <div class="flex items-center">
                    <button
                        class="btn btn-accent btn-outline rounded-full btn-sm"
                    >
                        {$_("remove")}
                    </button>
                </div>
            </div>
        {/each}
        <div class="p-2">
            <a
                href="/"
                on:click|preventDefault={onNewMember}
                class="flex p-2 space-x-4 ch"
            >
                <UserProfilePicture showPlus={true} size={42} />
                <div
                    class="grow flex flex-col font-bold justify-center text-primary"
                >
                    {$_("new-member")}
                </div>
            </a>
        </div>
    </div>
{/if}
