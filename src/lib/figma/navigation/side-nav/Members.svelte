<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import {
        userExpandOpen,
        toggleUserExpandOpen,
    } from "$lib/stores/dashboard";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    let { selected } = workspaceUserSearchModule;
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
