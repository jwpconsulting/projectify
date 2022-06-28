<script lang="ts">
    import {
        Mutation_AddUserToWorkspace,
        Mutation_RemoveUserFromWorkspace,
        Mutation_UpdateWorkspaceUser,
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
    import SearchInput from "../search-input.svelte";
    import Fuse from "fuse.js";
    import { fuseSearchThreshold } from "$lib/stores/dashboard";
    import DropdownButton from "../dropdown-button.svelte";
    import IconLockClosed from "../icons/icon-lock-closed.svelte";
    import { DropDownMenuItem, getDropDown } from "../globalDropDown.svelte";
    import { workspaceUserRoles } from "$lib/types/workspaceUserRole";
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import { validate } from "graphql";
    import { goto } from "$app/navigation";

    export let workspaceUUID = null;

    let res = null;
    let workspaceWSStore;
    let workspace = null;
    let customerByWorkspace = null;
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

            customerByWorkspace = $res.data["customerByWorkspace"];
        }
    }

    async function onNewMember() {
        let modalRes = await getModal("inviteTeamMemberToWorkspace").open();

        if (!modalRes) {
            return;
        }

        if (!modalRes.outputs?.email) {
            goto("/billing");
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

    async function onEditUser(user) {
        let modalRes = await getModal("editTeamMember").open(user);

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_UpdateWorkspaceUser,
                variables: {
                    input: {
                        workspaceUuid: workspaceUUID,
                        email: modalRes.outputs.email,
                        role: modalRes.outputs.role,
                        jobTitle: modalRes.outputs.jobTitle || "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    let roleFilter = null;
    let serachFieldEl;
    let searchText = "";
    let searchEngine = null;
    let filteredUsers;

    $: {
        filteredUsers = users || [];

        if (roleFilter) {
            console.log(filteredUsers);

            filteredUsers = filteredUsers.filter(
                (it) => it.role == roleFilter
            );
        }

        searchEngine = new Fuse(filteredUsers, {
            keys: ["email", "fullName"],
            threshold: fuseSearchThreshold,
        });

        if (searchText.length) {
            filteredUsers = searchEngine
                .search(searchText)
                .map((res) => res.item);
        }
    }

    let filterRoleButton;
    function openRolePicker() {
        let dropDown = getDropDown();

        let dropDownItems: DropDownMenuItem[] = [
            {
                label: $_("all-roles"),
                icon: null,
                onClick: () => {
                    roleFilter = null;
                },
            },
            ...workspaceUserRoles.map((role) => ({
                label: $_(role),
                icon: null,
                onClick: () => {
                    roleFilter = role;
                },
            })),
        ];

        dropDown.open(dropDownItems, filterRoleButton);
    }

    $: ownerRoleEmail = users?.find((it) => it.role == "OWNER")?.email || null;
</script>

{#if $res.loading}
    <div class="flex min-h-[200px] items-center justify-center">
        <Loading />
    </div>
{:else}
    <div class="flex gap-3 justify-center items-center py-4">
        <SearchInput
            placeholder={"Search for a team member"}
            bind:inputElement={serachFieldEl}
            bind:searchText
        />
        <DropdownButton
            label={roleFilter ? $_(roleFilter) : "Filter by role"}
            icon={IconLockClosed}
            bind:target={filterRoleButton}
            on:click={openRolePicker}
        />
    </div>
    <div class="divide-y divide-base-300">
        <table class="table-auto w-full">
            <thead>
                <tr class="text-left text-sm opacity-50">
                    <th class="px-2 py-4">{$_("member-details")}</th>
                    <th class="px-2 py-4">{$_("role")}</th>
                    <th class="px-2 py-4 text-right">{$_("edit-remove")}</th>
                </tr>
            </thead>
            <tbody>
                {#each filteredUsers as user}
                    <tr class="border-t border-base-300">
                        <td class="flex gap-4 p-2">
                            <div class="flex p-2">
                                <UserProfilePicture
                                    pictureProps={{
                                        url: user.profilePicture,
                                        size: 42,
                                    }}
                                />
                            </div>
                            <div
                                class="grow flex flex-col gap-2 justify-center"
                            >
                                <div class="font-bold">
                                    {user.fullName
                                        ? user.fullName
                                        : user.email}
                                </div>
                                {#if user.jobTitle}
                                    <div class="text-xs">{user.jobTitle}</div>
                                {/if}
                            </div>
                        </td>
                        <td class="p-2">{$_(user.role)}</td>
                        <td class="">
                            <div class="flex gap-2 items-end justify-end">
                                <button
                                    on:click={() => onEditUser(user)}
                                    class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                                    ><IconEdit /></button
                                >
                                <button
                                    on:click={() => onRemoveUser(user)}
                                    class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                                    ><IconTrash /></button
                                >
                            </div></td
                        >
                    </tr>
                {/each}
            </tbody>
        </table>
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
    {#if customerByWorkspace?.seatsRemaining}
        <ConfirmModalContent
            title={$_("invite-team-member")}
            confirmLabel={$_("send")}
            inputs={[
                {
                    name: "email",
                    label: $_("email"),
                    validation: {
                        required: true,
                    },
                    placeholder: $_("please-enter-a-email-of-team-member"),
                },
            ]}
        >
            <div class="text-center text-xs">
                {$_("you-have-seats-seats-left-in-your-plan", {
                    values: { seats: customerByWorkspace?.seatsRemaining },
                })}
            </div>
        </ConfirmModalContent>
    {:else}
        <ConfirmModalContent
            title={$_("invite-team-member")}
            confirmLabel={"Go to Billing"}
        >
            <div class="text-center text-xs text-error">
                {$_("you-have-0-seats-left-in-your-plan")}
            </div>
        </ConfirmModalContent>
    {/if}
</DialogModal>

<DialogModal id="removeTeamMemberFromWorkspace">
    <ConfirmModalContent
        title={$_("remove-team-member")}
        confirmLabel={$_("remove")}
        confirmColor="accent"
    >
        <div class="text-center text-xs">
            {$_("are-you-sure-you-want-to-remove-this-team-member")}
        </div>
    </ConfirmModalContent>
</DialogModal>

<DialogModal id="editTeamMember">
    <ConfirmModalContent
        title={$_("remove-team-member")}
        confirmLabel={$_("remove")}
        confirmColor="accent"
    >
        {"Ed"}
    </ConfirmModalContent>
</DialogModal>

<DialogModal id="editTeamMember">
    <ConfirmModalContent
        title={$_("edit-team-member")}
        confirmLabel={$_("Save")}
        inputs={[
            {
                name: "fullName",
                label: $_("name-0"),
                validation: { required: false },
            },
            {
                name: "email",
                label: $_("email-0"),
                validation: { required: true },
            },
            {
                name: "jobTitle",
                label: $_("job-title"),
                validation: { required: false },
            },
            {
                name: "role",
                label: $_("permissions"),
                type: "select",
                placeholder: $_("selecat-a-permission"),
                selectOptions: workspaceUserRoles.map((role) => ({
                    label: $_(role),
                    value: role,
                })),
                validation: {
                    required: true,
                    validator: (value, data) => {
                        console.log(value, ownerRoleEmail, data.email);

                        if (
                            value == "OWNER" &&
                            ownerRoleEmail &&
                            ownerRoleEmail != data.email
                        ) {
                            return {
                                error: true,
                                message: $_(
                                    "you-can-only-assign-one-owner-per-workspace-please-choose-another-role"
                                ),
                            };
                        }
                    },
                },
            },
        ]}
    />
</DialogModal>
