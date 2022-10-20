<script lang="ts">
    import SquovalIcon from "$lib/figma/buttons/SquovalIcon.svelte";
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import {
        currentWorkspace,
        selectedWorkspaceUser,
        selectWorkspaceUser,
        deselectWorkspaceUser,
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="member"
        on:click={toggleUserExpandOpen}
        active={$selectedWorkspaceUser.kind === "workspaceUsers"}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectUserClosedNav
                user={null}
                active={$selectedWorkspaceUser.kind === "unassigned"}
                on:select={() => selectWorkspaceUser({ kind: "unassigned" })}
                on:deselect={() =>
                    deselectWorkspaceUser({ kind: "unassigned" })}
            />
            {#if $currentWorkspace && $currentWorkspace.workspace_users}
                {#each $currentWorkspace.workspace_users as workspaceUser}
                    <SelectUserClosedNav
                        user={workspaceUser.user}
                        active={$selectedWorkspaceUser.kind ===
                            "workspaceUsers" &&
                            $selectedWorkspaceUser.workspaceUserUuids.has(
                                workspaceUser.uuid
                            )}
                        on:select={() =>
                            selectWorkspaceUser({
                                kind: "workspaceUser",
                                workspaceUser,
                            })}
                        on:deselect={() =>
                            deselectWorkspaceUser({
                                kind: "workspaceUser",
                                workspaceUser,
                            })}
                    />
                {/each}
            {/if}
        </div>
    {/if}
</div>
