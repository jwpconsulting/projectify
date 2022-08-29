<script lang="ts">
    import WorkspaceMenu from "$lib/figma/WorkspaceMenu.svelte";
    import SideNavBoards from "./SideNavBoards.svelte";
    import SideNavMembers from "./SideNavMembers.svelte";
    import FilterLabelCollapsible from "$lib/figma/FilterLabelCollapsible.svelte";
    import SideNavBulkSelect from "./SideNavBulkSelect.svelte";
</script>

<nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
    <WorkspaceMenu />
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <SideNavBoards />
        <SideNavMembers />
        <FilterLabelCollapsible />
        <SideNavBulkSelect />
    </div>
</nav>
