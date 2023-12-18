<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
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
    import type {
        WorkspaceUserAssignmentState,
        WorkspaceUserSelection,
    } from "$lib/types/ui";
    import type { WorkspaceUser } from "$lib/types/workspace";

    type FilterWorkspaceUserMenuMode =
        | { kind: "filter" }
        | { kind: "assign"; workspaceUserAssignment: WorkspaceUserAssignment };

    export let mode: FilterWorkspaceUserMenuMode;

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

    function isSelected(
        $selected: WorkspaceUserAssignmentState | WorkspaceUserSelection,
        workspaceUser: WorkspaceUser
    ): boolean {
        if ($selected.kind === "workspaceUsers") {
            return $selected.workspaceUserUuids.has(workspaceUser.uuid);
        } else if ($selected.kind === "workspaceUser") {
            return workspaceUser.uuid === $selected.workspaceUser.uuid;
        }
        return false;
    }
</script>

<!-- TODO remove px/pt here -->
<div class="flex flex-col px-4 pt-2">
    <InputField
        bind:value={$workspaceUserSearch}
        style={{ inputType: "text" }}
        label={$_("dashboard.filter-workspace-users")}
        name="workspace-user-name"
        placeholder={$_("dashboard.workspace-user-name")}
    >
        <Icon
            slot="left"
            src={Search}
            class="w-4"
            theme="outline"
        /></InputField
    >
</div>
<div class="flex flex-col">
    <FilterUser
        workspaceUserSelectionInput={{ kind: "unassigned" }}
        active={$selected.kind === "unassigned"}
        count={$tasksPerUser.unassigned}
        onSelect={() => select({ kind: "unassigned" })}
        onDeselect={() => deselect({ kind: "unassigned" })}
    />
    {#each $workspaceUserSearchResults as workspaceUser (workspaceUser.uuid)}
        <FilterUser
            workspaceUserSelectionInput={{
                kind: "workspaceUser",
                workspaceUser: workspaceUser,
            }}
            active={isSelected($selected, workspaceUser)}
            count={$tasksPerUser.assigned.get(workspaceUser.uuid)}
            onSelect={() =>
                select({
                    kind: "workspaceUser",
                    workspaceUser: workspaceUser,
                })}
            onDeselect={() =>
                deselect({
                    kind: "workspaceUser",
                    workspaceUser: workspaceUser,
                })}
        />
    {/each}
</div>
