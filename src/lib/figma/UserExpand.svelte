<script lang="ts">
    import Squoval from "$lib/figma/Squoval.svelte";
    import FilterUserAvatar from "$lib/figma/FilterUserAvatar.svelte";
    import {
        currentWorkspace,
        selectedWorkspaceUser,
        selectWorkspaceUser,
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
</script>

<div class="flex flex-col items-center gap-6">
    <Squoval
        state="active"
        icon="member"
        on:click={toggleUserExpandOpen}
        active={$selectedWorkspaceUser.kind === "workspaceUser"}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <FilterUserAvatar
                user={null}
                active={$selectedWorkspaceUser.kind === "unassigned"}
                on:click={() => selectWorkspaceUser({ kind: "unassigned" })}
            />
            {#if $currentWorkspace && $currentWorkspace.workspace_users}
                {#each $currentWorkspace.workspace_users as workspaceUser}
                    <FilterUserAvatar
                        user={workspaceUser.user}
                        active={$selectedWorkspaceUser.kind ===
                            "workspaceUser" &&
                            $selectedWorkspaceUser.workspaceUserUuid ===
                                workspaceUser.uuid}
                        on:click={() =>
                            selectWorkspaceUser({
                                kind: "workspaceUser",
                                workspaceUser,
                            })}
                    />
                {/each}
            {/if}
        </div>
    {/if}
</div>
