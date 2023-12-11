<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import FilterWorkspaceUser from "$lib/figma/composites/FilterWorkspaceUser.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
    import { selectedWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
</script>

<SideNavMenuCategory
    label={$_("dashboard.workspace-users")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selectedWorkspaceUser.kind !== "allWorkspaceUsers"}
/>
{#if $userExpandOpen}
    <div class="shrink overflow-y-auto">
        <FilterWorkspaceUser mode={{ kind: "filter" }} />
    </div>
{/if}
