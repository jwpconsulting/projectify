<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
    import { workspaceUserFilter } from "$lib/stores/dashboard/workspaceUserFilter";

    const { selected } = workspaceUserFilter;
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.members")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selected.kind !== "allWorkspaceUsers"}
/>
{#if $userExpandOpen}
    <FilterMemberMenu {workspaceUserFilter} />
{/if}
