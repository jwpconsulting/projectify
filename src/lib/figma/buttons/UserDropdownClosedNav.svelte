<script lang="ts">
    // TODO rename WorkspaceUserDropdownClosedNav
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import {
        workspaceUserFilter,
        filterByWorkspaceUser,
        unfilterByWorkspaceUser,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard/workspaceUserFilter";
    // TODO refactor these
    // Maybe a module like SideNavExpandStatesModule

    const { selected } = workspaceUserFilter;
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="member"
        action={{ kind: "button", action: toggleUserExpandOpen }}
        active={$selected.kind === "workspaceUsers"}
    />
    {#if $userExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectUserClosedNav
                user={null}
                active={$selected.kind === "unassigned"}
                on:select={() => filterByWorkspaceUser({ kind: "unassigned" })}
                on:deselect={() =>
                    unfilterByWorkspaceUser({ kind: "unassigned" })}
            />
            {#each $workspaceUserSearchResults as workspaceUser}
                <SelectUserClosedNav
                    user={workspaceUser.user}
                    active={$selected.kind === "workspaceUsers" &&
                        $selected.workspaceUserUuids.has(workspaceUser.uuid)}
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
