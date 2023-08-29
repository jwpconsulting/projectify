<script lang="ts">
    import Fuse from "fuse.js";
    import { _ } from "svelte-i18n";

    import { fuseSearchThreshold } from "$lib/config";

    import IconEdit from "$lib/components/icons/icon-edit.svelte";
    import IconTrash from "$lib/components/icons/icon-trash.svelte";
    import {
        currentCustomer,
        currentWorkspace,
        loading,
    } from "$lib/stores/dashboard";
    import type { WorkspaceUser } from "$lib/types/workspace";

    let workspaceUsers: WorkspaceUser[] = [];

    // TODO currentWorkspace shall instead be passing a by +page.ts

    $: {
        $loading = !($currentWorkspace && $currentCustomer);
    }
    $: {
        if ($currentWorkspace?.workspace_users) {
            workspaceUsers = $currentWorkspace.workspace_users;
        }
    }

    async function onNewMember() {
        // TODO if (!modalRes.outputs?.email) {
        // TODO     goto("/billing");
        // TODO     return;
        // TODO }
        // TODO if (!$currentWorkspace) {
        // TODO     return;
        // TODO }
        // TODO await client.mutate({
        // TODO     mutation: Mutation_AddUserToWorkspace,
        // TODO     variables: {
        // TODO         input: {
        // TODO             uuid: $currentWorkspace.uuid,
        // TODO             email: modalRes.outputs.email,
        // TODO         },
        // TODO     },
        // TODO });
    }
    async function onRemoveUser(workspaceUser: WorkspaceUser) {
        console.error("TODO remove", workspaceUser);
        await new Promise(console.error);
        // TODO if (!$currentWorkspace) {
        // TODO     return;
        // TODO }
        // TODO await client.mutate({
        // TODO     mutation: Mutation_RemoveUserFromWorkspace,
        // TODO     variables: {
        // TODO         input: {
        // TODO             uuid: $currentWorkspace.uuid,
        // TODO             email: workspaceUser.user.email,
        // TODO         },
        // TODO     },
        // TODO });
    }

    async function onEditUser(workspaceUser: WorkspaceUser) {
        console.error("TODO edit", workspaceUser);
        await new Promise(console.error);
        // TODO if (!$currentWorkspace) {
        // TODO     return;
        // TODO }
        // TODO await client.mutate({
        // TODO     mutation: Mutation_UpdateWorkspaceUser,
        // TODO     variables: {
        // TODO         input: {
        // TODO             workspaceUuid: $currentWorkspace.uuid,
        // TODO             email: modalRes.outputs.email,
        // TODO             role: modalRes.outputs.role,
        // TODO             jobTitle: modalRes.outputs.job_title || "",
        // TODO         },
        // TODO     },
        // TODO });
    }

    let roleFilter: string | null = null;
    let searchText = "";
    let filteredWorkspaceUsers: WorkspaceUser[];

    $: {
        filteredWorkspaceUsers = workspaceUsers;

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
</script>

<div class="flex items-center justify-center gap-3 py-4">
    <!-- TODO add search input -->
    <!-- TODO show dropdown button here? -->
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
                            TODO: A user profile picture may be shown here
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
            TODO: Show a profile picture here
            <div
                class="flex grow flex-col justify-center font-bold text-primary"
            >
                {$_("new-member")}
            </div>
        </a>
    </div>
</div>
