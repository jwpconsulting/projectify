<script lang="ts">
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { WorkspaceUserFilter } from "$lib/types/stores";

    export let workspaceUserFilter: WorkspaceUserFilter;
</script>

<Layout>
    <FilterMemberMenu {workspaceUserFilter} />
</Layout>
