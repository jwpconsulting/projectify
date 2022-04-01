<script lang="ts">
    import {
        Mutation_AddUserToWorkspace,
        Mutation_RemoveUserFromWorkspace,
        Query_WorkspaceTeamMembers,
    } from "$lib/graphql/operations";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";

    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import Loading from "../loading.svelte";
    import ProfilePicture from "../profilePicture.svelte";
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { client } from "$lib/graphql/client";
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

    async function onNewMember() {
        let modalRes = await getModal("inviteTeamMemberToWorkspace").open();

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_AddUserToWorkspace,
                variables: {
                    input: {
                        uuid: workspaceUUID,
                        email: modalRes.outputs.email,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }
    async function onRemoveUser(user) {
        let modalRes = await getModal("removeTeamMemberFromWorkspace").open();

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_RemoveUserFromWorkspace,
                variables: {
                    input: {
                        uuid: workspaceUUID,
                        email: user.email,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }
</script>

{#if $res.loading}
    <div class="flex min-h-[200px] items-center justify-center">
        <Loading />
    </div>
{:else}
    <div class=" divide-y divide-base-300">
        {#each users as user}
            <div class="flex px-4 py-4 space-x-4">
                <UserProfilePicture
                    pictureProps={{
                        url: user.profilePicture,
                        size: 42,
                    }}
                />

                <div class="grow flex flex-col  justify-center">
                    <div class="text-xs">Interface designer</div>
                    <div class="font-bold">
                        {user.fullName ? user.fullName : user.email}
                    </div>
                </div>
                <div class="flex items-center">
                    <button
                        on:click={() => onRemoveUser(user)}
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
                <ProfilePicture showPlus={true} size={42} />
                <div
                    class="grow flex flex-col font-bold justify-center text-primary"
                >
                    {$_("new-member")}
                </div>
            </a>
        </div>
    </div>
{/if}

<DialogModal id="inviteTeamMemberToWorkspace">
    <ConfirmModalContent
        title={"Invite team member"}
        subtitle={"Please enter a email of team member."}
        confirmLabel={"Send"}
        inputs={[
            {
                name: "email",
                label: "Email",
                placeholder: "Please enter a email of team member.",
            },
        ]}
    />
</DialogModal>

<DialogModal id="removeTeamMemberFromWorkspace">
    <ConfirmModalContent
        title={"Remove team member"}
        confirmLabel={"Remove"}
        confirmColor="accent"
    >
        {"Are you sure you want to remove this team member?"}
    </ConfirmModalContent>
</DialogModal>
