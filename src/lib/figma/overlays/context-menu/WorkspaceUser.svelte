<script lang="ts">
    // Rename consistent with the other context menus
    import FilterWorkspaceUser from "$lib/figma/composites/FilterWorkspaceUser.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { WorkspaceUserAssignment } from "$lib/types/stores";

    export let workspaceUserAssignment: WorkspaceUserAssignment;
</script>

<Layout>
    <FilterWorkspaceUser mode={{ kind: "assign", workspaceUserAssignment }} />
</Layout>
