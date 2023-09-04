<script lang="ts">
    import { _ } from "svelte-i18n";

    import FilterUser from "$lib/figma/select-controls/FilterUser.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    let { select, deselect, selected, tasksPerUser, search, searchResults } =
        workspaceUserSearchModule;
</script>

<div class="flex flex-col px-4 pb-4 pt-2">
    <div class="color-base-content p-2 text-xs font-bold capitalize">
        {$_("dashboard.filter-members")}
    </div>
    <InputField
        bind:value={$search}
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
        on:select={() => select({ kind: "unassigned" })}
        on:deselect={() => deselect({ kind: "unassigned" })}
    />
    {#each $searchResults as workspaceUser (workspaceUser.uuid)}
        <FilterUser
            workspaceUserSelectionInput={{
                kind: "workspaceUser",
                workspaceUser: workspaceUser,
            }}
            active={$selected.kind === "workspaceUsers"
                ? $selected.workspaceUserUuids.has(workspaceUser.uuid)
                : false}
            count={$tasksPerUser.assigned.get(workspaceUser.uuid)}
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
