<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
        workspaceUserSearchModule,
    } from "$lib/stores/dashboard";

    const { selected } = workspaceUserSearchModule;
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.members")}
    icon={User}
    open={$userExpandOpen}
    on:click={toggleUserExpandOpen}
    filtered={$selected.kind !== "allWorkspaceUsers"}
/>
{#if $userExpandOpen}
    <FilterMemberMenu {workspaceUserSearchModule} />
{/if}
