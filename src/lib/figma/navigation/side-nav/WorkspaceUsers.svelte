<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import FilterWorkspaceUser from "$lib/figma/composites/FilterWorkspaceUser.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
    import { selectedWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.workspace-users")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selectedWorkspaceUser.kind !== "allWorkspaceUsers"}
/>
{#if $userExpandOpen}
    <FilterWorkspaceUser mode={{ kind: "filter" }} />
{/if}
