<script lang="ts">
    // Rename consistent with the other context menus
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { WorkspaceUserAssignment } from "$lib/types/stores";

    export let workspaceUserAssignment: WorkspaceUserAssignment;
</script>

<Layout>
    <FilterMemberMenu mode={{ kind: "assign", workspaceUserAssignment }} />
</Layout>
