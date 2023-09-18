<script lang="ts">
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { WorkspaceUserSearchStore } from "$lib/types/stores";

    export let workspaceUserFilter: WorkspaceUserSearchStore;
</script>

<Layout>
    <FilterMemberMenu {workspaceUserFilter} />
</Layout>
