<script lang="ts">
    import WorkspaceMenu from "$lib/components/dashboard/WorkspaceMenu.svelte";
    import Boards from "$lib/figma/navigation/side-nav/Boards.svelte";
    import Members from "$lib/figma/navigation/side-nav/Members.svelte";
    import FilterLabelCollapsible from "$lib/figma/composites/FilterLabelCollapsible.svelte";
</script>

<nav class="flex h-full w-72 shrink-0 flex-col bg-base-100 py-4 pr-px">
    <WorkspaceMenu />
    <div class="flex flex-col overflow-x-auto overflow-y-scroll">
        <Boards />
        <Members />
        <FilterLabelCollapsible />
    </div>
</nav>
