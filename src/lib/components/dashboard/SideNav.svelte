<script lang="ts">
    import WorkspaceMenu from "$lib/components/dashboard/WorkspaceMenu.svelte";
    import SideNavBoards from "$lib/components/dashboard/SideNavBoards.svelte";
    import SideNavMembers from "$lib/components/dashboard/SideNavMembers.svelte";
    import FilterLabelCollapsible from "$lib/figma/composites/FilterLabelCollapsible.svelte";
    import SideNavBulkSelect from "$lib/components/dashboard/SideNavBulkSelect.svelte";
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
