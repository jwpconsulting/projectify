<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";
    import SideNavMenuCategoryFocus from "$lib/figma/SideNavMenuCategoryFocus.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import SearchField from "$lib/components/SearchField.svelte";
    import type { WorkspaceUser } from "$lib/types";
    import Fuse from "fuse.js";
    import {
        selectedWorkspaceUser,
        fuseSearchThreshold,
    } from "$lib/stores/dashboard";
    import FilterWorkspaceUser from "$lib/components/FilterWorkspaceUser.svelte";

    let open = true;
    let searchInput = "";

    let workspaceUsers: WorkspaceUser[] = [];
    $: {
        const defaultWorkspaceUsers = $currentWorkspace
            ? $currentWorkspace.workspace_users || []
            : [];
        workspaceUsers =
            searchInput === ""
                ? defaultWorkspaceUsers
                : search(defaultWorkspaceUsers, searchInput);
    }

    function search(workspaceUsers: WorkspaceUser[], searchInput: string) {
        const searchEngine = new Fuse(workspaceUsers, {
            keys: ["user.email", "user.full_name"],
            threshold: fuseSearchThreshold,
            shouldSort: false,
        });
        const result = searchEngine.search(searchInput);
        return result.map((res: Fuse.FuseResult<WorkspaceUser>) => res.item);
    }

    function toggleOpen() {
        open = !open;
    }
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.members")}
    icon={User}
    {open}
    on:click={toggleOpen}
    filtered={$selectedWorkspaceUser.kind !== "allWorkspaceUsers"}
/>
{#if open}
    <div class="flex flex-col px-4 pt-2 pb-4">
        <div class="color-base-content p-2 text-xs font-bold capitalize">
            {$_("dashboard.filter-members")}
        </div>
        <SearchField
            bind:searchInput
            placeholder={$_("dashboard.member-name")}
        />
    </div>
    <div class="flex flex-col">
        <FilterWorkspaceUser workspaceUser={{ kind: "unassigned" }} />
        {#each workspaceUsers as workspaceUser (workspaceUser.uuid)}
            <FilterWorkspaceUser
                workspaceUser={{
                    kind: "workspaceUser",
                    workspaceUser: workspaceUser,
                }}
            />
        {/each}
    </div>
{/if}
