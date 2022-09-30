<script lang="ts">
    import {
        Mutation_AddUserToWorkspace,
        Mutation_RemoveUserFromWorkspace,
        Mutation_UpdateWorkspaceUser,
    } from "$lib/graphql/operations";
    import type { WorkspaceUser } from "$lib/types/workspace";

    import { _ } from "svelte-i18n";
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import DialogModal, { getModal } from "$lib/components/dialogModal.svelte";
    import ConfirmModalContent from "$lib/components/confirmModalContent.svelte";
    import { client } from "$lib/graphql/client";
    import UserProfilePicture from "$lib/components/userProfilePicture.svelte";
    import SearchInput from "$lib/components/search-input.svelte";
    import Fuse from "fuse.js";
    import { fuseSearchThreshold } from "$lib/stores/dashboard";
    import DropdownButton from "$lib/components/dropdown-button.svelte";
    import IconLockClosed from "$lib/components/icons/icon-lock-closed.svelte";
    import { getDropDown } from "$lib/components/globalDropDown.svelte";
    import type { DropDownMenuItem } from "$lib/components/globalDropDown.svelte";
    import { workspaceUserRoles } from "$lib/types/workspaceUserRole";
    import IconEdit from "$lib/components/icons/icon-edit.svelte";
    import IconTrash from "$lib/components/icons/icon-trash.svelte";
    import { goto } from "$app/navigation";
    import {
        loading,
        currentWorkspace,
        currentCustomer,
    } from "$lib/stores/dashboard";
    import type { Input } from "$lib/types/ui";

    let workspaceUsers: WorkspaceUser[] = [];

    $: {
        $loading = !($currentWorkspace && $currentCustomer);
    }
    $: {
        if ($currentWorkspace && $currentWorkspace.workspace_users) {
            workspaceUsers = $currentWorkspace.workspace_users;
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

        if (!$currentWorkspace) {
            return;
        }

        await client.mutate({
            mutation: Mutation_AddUserToWorkspace,
            variables: {
                input: {
                    uuid: $currentWorkspace.uuid,
                    email: modalRes.outputs.email,
                },
            },
        });
    }
    async function onRemoveUser(workspaceUser: WorkspaceUser) {
        let modalRes = await getModal("removeTeamMemberFromWorkspace").open();

        if (!modalRes) {
            return;
        }

        if (!$currentWorkspace) {
            return;
        }

        await client.mutate({
            mutation: Mutation_RemoveUserFromWorkspace,
            variables: {
                input: {
                    uuid: $currentWorkspace.uuid,
                    email: workspaceUser.user.email,
                },
            },
        });
    }

    async function onEditUser(workspaceUser: WorkspaceUser) {
        let modalRes = await getModal("editTeamMember").open(workspaceUser);

        if (!modalRes) {
            return;
        }

        if (!$currentWorkspace) {
            return;
        }

        await client.mutate({
            mutation: Mutation_UpdateWorkspaceUser,
            variables: {
                input: {
                    workspaceUuid: $currentWorkspace.uuid,
                    email: modalRes.outputs.email,
                    role: modalRes.outputs.role,
                    jobTitle: modalRes.outputs.job_title || "",
                },
            },
        });
    }

    let roleFilter: string | null = null;
    let searchFieldEl: HTMLElement;
    let searchText = "";
    let filteredWorkspaceUsers: WorkspaceUser[];

    $: {
        filteredWorkspaceUsers = workspaceUsers || [];

        if (roleFilter) {
            console.log(filteredWorkspaceUsers);

            filteredWorkspaceUsers = filteredWorkspaceUsers.filter(
                (it) => it.role == roleFilter
            );
        }

        const searchEngine = new Fuse(filteredWorkspaceUsers, {
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

    let filterRoleButton: HTMLElement | null;
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

        if (dropDown && filterRoleButton) {
            dropDown.open(dropDownItems, filterRoleButton);
        } else {
            throw new Error("Expected dropDown && filterRoleButton");
        }
    }

    let editTeamMemberInputs: Input[];
    $: {
        editTeamMemberInputs = [
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
        ];
    }
    let inviteTeamMemberInputs: Input[];
    $: {
        inviteTeamMemberInputs = [
            {
                name: "email",
                label: $_("email"),
                validation: {
                    required: true,
                },
                placeholder: $_("please-enter-a-email-of-team-member"),
            },
        ];
    }
</script>

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
                                    url: workspaceUser.user.profile_picture,
                                    size: 42,
                                }}
                            />
                        </div>
                        <div class="flex grow flex-col justify-center gap-2">
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
                                on:click={() => onRemoveUser(workspaceUser)}
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
<DialogModal id="inviteTeamMemberToWorkspace">
    {#if $currentCustomer?.seats_remaining}
        <ConfirmModalContent
            title={$_("invite-team-member")}
            confirmLabel={$_("send")}
            inputs={inviteTeamMemberInputs}
        >
            <div class="text-center text-xs">
                {$_("you-have-seats-seats-left-in-your-plan", {
                    values: { seats: $currentCustomer.seats_remaining },
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
        inputs={editTeamMemberInputs}
    />
</DialogModal>
