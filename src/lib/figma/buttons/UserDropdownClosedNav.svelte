<script lang="ts">
    // TODO rename WorkspaceUserDropdownClosedNav
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import {
        selectedWorkspaceUser,
        filterByWorkspaceUser,
        unfilterByWorkspaceUser,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard/workspaceUserFilter";
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="workspaceUser"
        action={{ kind: "button", action: toggleUserExpandOpen }}
        active={$selectedWorkspaceUser.kind === "workspaceUsers"}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectUserClosedNav
                user={undefined}
                active={$selectedWorkspaceUser.kind === "unassigned"}
                on:select={() => filterByWorkspaceUser({ kind: "unassigned" })}
                on:deselect={() =>
                    unfilterByWorkspaceUser({ kind: "unassigned" })}
            />
            {#each $workspaceUserSearchResults as workspaceUser}
                <SelectUserClosedNav
                    user={workspaceUser.user}
                    active={$selectedWorkspaceUser.kind === "workspaceUsers" &&
                        $selectedWorkspaceUser.workspaceUserUuids.has(
                            workspaceUser.uuid
                        )}
                    on:select={() =>
                        filterByWorkspaceUser({
                            kind: "workspaceUser",
                            workspaceUser,
                        })}
                    on:deselect={() =>
                        unfilterByWorkspaceUser({
                            kind: "workspaceUser",
                            workspaceUser,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
