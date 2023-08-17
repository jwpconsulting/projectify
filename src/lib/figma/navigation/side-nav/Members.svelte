<script lang="ts">
    import { User } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import SideNavMenuCategoryFocus from "$lib/figma/buttons/SideNavMenuCategoryFocus.svelte";
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
    let { selected } = workspaceUserSearchModule;

    let open = true;

    function toggleOpen() {
        open = !open;
    }
</script>

<SideNavMenuCategoryFocus
    label={$_("dashboard.members")}
    icon={User}
    {open}
    on:click={toggleOpen}
    filtered={$selected.kind !== "allWorkspaceUsers"}
/>
{#if open}
    <FilterMemberMenu {workspaceUserSearchModule} />
{/if}
