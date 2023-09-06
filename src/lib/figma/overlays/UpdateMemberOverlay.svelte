<script lang="ts">
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
</script>

<Layout>
    <FilterMemberMenu {workspaceUserSearchModule} />
</Layout>
