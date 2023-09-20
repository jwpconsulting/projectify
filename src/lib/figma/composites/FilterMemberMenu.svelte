<script lang="ts">
    import { _ } from "svelte-i18n";

    import FilterUser from "$lib/figma/select-controls/FilterUser.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { tasksPerUser } from "$lib/stores/dashboard";
    import {
        filterByWorkspaceUser,
        selectedWorkspaceUser,
        unfilterByWorkspaceUser,
        workspaceUserSearch,
        workspaceUserSearchResults,
    } from "$lib/stores/dashboard/workspaceUserFilter";
    import type { WorkspaceUserAssignment } from "$lib/types/stores";

    type FilterMemberMenuMode =
        | { kind: "filter" }
        | { kind: "assign"; workspaceUserAssignment: WorkspaceUserAssignment };

    // TODO make non-optional
    export let mode: FilterMemberMenuMode = { kind: "filter" };

    $: selected =
        mode.kind === "filter"
            ? selectedWorkspaceUser
            : mode.workspaceUserAssignment.selected;
    $: select =
        mode.kind === "filter"
            ? filterByWorkspaceUser
            : mode.workspaceUserAssignment.select;
    $: deselect =
        mode.kind === "filter"
            ? unfilterByWorkspaceUser
            : mode.workspaceUserAssignment.deselect;

    // TODO The whole above could be turned into a store
</script>

<div class="flex flex-col px-4 pb-4 pt-2">
    <div class="color-base-content p-2 text-xs font-bold capitalize">
        {$_("dashboard.filter-members")}
    </div>
    <InputField
        bind:value={$workspaceUserSearch}
        style={{ kind: "search" }}
        name="member-name"
        placeholder={$_("dashboard.member-name")}
    />
</div>
<div class="flex flex-col">
    <FilterUser
        workspaceUserSelectionInput={{ kind: "unassigned" }}
        active={$selected.kind === "unassigned"}
        count={$tasksPerUser.unassigned}
        onSelect={select}
        onDeselect={deselect}
    />
    {#each $workspaceUserSearchResults as workspaceUser (workspaceUser.uuid)}
        <FilterUser
            workspaceUserSelectionInput={{
                kind: "workspaceUser",
                workspaceUser: workspaceUser,
            }}
            active={$selected.kind === "workspaceUsers"
                ? $selected.workspaceUserUuids.has(workspaceUser.uuid)
                : false}
            count={$tasksPerUser.assigned.get(workspaceUser.uuid)}
            onSelect={select}
            onDeselect={deselect}
        />
    {/each}
</div>
