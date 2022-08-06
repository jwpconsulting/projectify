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

    let active: boolean;
    $: {
        active = $selectedWorkspaceUser !== null;
    }
</script>

<div class="flex flex-col items-center gap-6">
    <Squoval
        state="active"
        icon="member"
        on:click={toggleUserExpandOpen}
        {active}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <FilterUserAvatar
                user={null}
                active={$selectedWorkspaceUser === "unassigned"}
                on:click={() => selectWorkspaceUser("unassigned")}
            />
            {#if $currentWorkspace && $currentWorkspace.workspace_users}
                {#each $currentWorkspace.workspace_users as workspaceUser}
                    <FilterUserAvatar
                        user={workspaceUser.user}
                        active={$selectedWorkspaceUser !== "unassigned" &&
                        $selectedWorkspaceUser !== null
                            ? $selectedWorkspaceUser.uuid ===
                              workspaceUser.uuid
                            : false}
                        on:click={() => selectWorkspaceUser(workspaceUser)}
                    />
                {/each}
            {/if}
        </div>
    {/if}
</div>
