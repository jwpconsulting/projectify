<script lang="ts">
    import SelectUserClosedNav from "$lib/figma/buttons/SelectUserClosedNav.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    // TODO refactor these
    // Maybe a module like SideNavExpandStatesModule
    import {
        toggleUserExpandOpen,
        userExpandOpen,
    } from "$lib/stores/dashboard/ui";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    let { select, deselect, selected, searchResults } =
        workspaceUserSearchModule;
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
                on:select={() => select({ kind: "unassigned" })}
                on:deselect={() => deselect({ kind: "unassigned" })}
            />
            {#each $searchResults as workspaceUser}
                <SelectUserClosedNav
                    user={workspaceUser.user}
                    active={$selected.kind === "workspaceUsers" &&
                        $selected.workspaceUserUuids.has(workspaceUser.uuid)}
                    on:select={() =>
                        select({
                            kind: "workspaceUser",
                            workspaceUser,
                        })}
                    on:deselect={() =>
                        deselect({
                            kind: "workspaceUser",
                            workspaceUser,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
