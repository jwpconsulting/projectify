<script lang="ts">
    import {
        Mutation_AddUserToWorkspace,
        Mutation_RemoveUserFromWorkspace,
        Mutation_UpdateWorkspaceUser,
    } from "$lib/graphql/operations";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import { getWorkspaceCustomer, getWorkspace } from "$lib/repository";
    import type { Customer, Workspace, WorkspaceUser } from "$lib/types";

    import debounce from "lodash/debounce.js";
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
    import { getDropDown } from "../globalDropDown.svelte";
    import type { DropDownMenuItem } from "../globalDropDown.svelte";
    import { workspaceUserRoles } from "$lib/types/workspaceUserRole";
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import { goto } from "$app/navigation";
    import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";

    export let workspaceUUID = null;

    let loading = true;
    let customer: Customer | null = null;
    let workspaceWSStore: WSSubscriptionStore;
    let workspace: Workspace | null = null;
    let workspaceUsers: WorkspaceUser[] | null = null;

    async function fetch() {
        [customer, workspace] = await Promise.all([
            getWorkspaceCustomer(workspaceUUID),
            getWorkspace(workspaceUUID),
        ]);
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
        if (!loading) {
            workspaceUsers = workspace.workspace_users;
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
    async function onRemoveUser(workspaceUser: WorkspaceUser) {
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
                        email: workspaceUser.user.email,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onEditUser(workspaceUser: WorkspaceUser) {
        let modalRes = await getModal("editTeamMember").open(workspaceUser);

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
                        jobTitle: modalRes.outputs.job_title || "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    let roleFilter = null;
    let searchFieldEl: HTMLElement;
    let searchText = "";
    let searchEngine: Fuse<WorkspaceUser> = null;
    let filteredWorkspaceUsers: WorkspaceUser[] | null;

    $: {
        filteredWorkspaceUsers = workspaceUsers || [];

        if (roleFilter) {
            console.log(filteredWorkspaceUsers);

            filteredWorkspaceUsers = filteredWorkspaceUsers.filter(
                (it) => it.role == roleFilter
            );
        }

        searchEngine = new Fuse(filteredWorkspaceUsers, {
            keys: ["user.email", "user.full_name"],
            threshold: fuseSearchThreshold,
        });

        if (searchText.length) {
            const result = searchEngine.search(searchText);
            filteredWorkspaceUsers = result.map(
                (res: Fuse.FuseResult<WorkspaceUser>) => res.item
            );
        }
    }

    let filterRoleButton: HTMLElement;
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
</script>

{#if loading}
    <div class="flex min-h-[200px] items-center justify-center">
        <Loading />
    </div>
{:else}
    <div class="flex items-center justify-center gap-3 py-4">
        <SearchInput
            placeholder={"Search for a team member"}
            bind:inputElement={searchFieldEl}
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
        <table class="w-full table-auto">
            <thead>
                <tr class="text-left text-sm opacity-50">
                    <th class="px-2 py-4">{$_("member-details")}</th>
                    <th class="px-2 py-4">{$_("role")}</th>
                    <th class="px-2 py-4 text-right">{$_("edit-remove")}</th>
                </tr>
            </thead>
            <tbody>
                {#each filteredWorkspaceUsers as workspaceUser}
                    <tr class="border-t border-base-300">
                        <td class="flex gap-4 p-2">
                            <div class="flex p-2">
                                <UserProfilePicture
                                    pictureProps={{
                                        url: workspaceUser.user
                                            .profile_picture,
                                        size: 42,
                                    }}
                                />
                            </div>
                            <div
                                class="flex grow flex-col justify-center gap-2"
                            >
                                <div class="font-bold">
                                    {workspaceUser.user.full_name
                                        ? workspaceUser.user.full_name
                                        : workspaceUser.user.email}
                                </div>
                                {#if workspaceUser.job_title}
                                    <div class="text-xs">
                                        {workspaceUser.job_title}
                                    </div>
                                {/if}
                            </div>
                        </td>
                        <td class="p-2">{$_(workspaceUser.role)}</td>
                        <td class="">
                            <div class="flex items-end justify-end gap-2">
                                <button
                                    on:click={() => onEditUser(workspaceUser)}
                                    class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                                    ><IconEdit /></button
                                >
                                <button
                                    on:click={() =>
                                        onRemoveUser(workspaceUser)}
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
                class="ch flex space-x-4 p-2"
            >
                <ProfilePicture showPlus={true} size={42} />
                <div
                    class="flex grow flex-col justify-center font-bold text-primary"
                >
                    {$_("new-member")}
                </div>
            </a>
        </div>
    </div>
{/if}

<DialogModal id="inviteTeamMemberToWorkspace">
    {#if customer?.seats_remaining}
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
                    values: { seats: customer.seats_remaining },
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
                name: "user.full_name",
                label: $_("name-0"),
                readonly: true,
                validation: { required: false },
            },
            {
                name: "user.email",
                label: $_("email-0"),
                readonly: true,
                validation: { required: true },
            },
            {
                name: "job_title",
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
                },
            },
        ]}
    />
</DialogModal>
