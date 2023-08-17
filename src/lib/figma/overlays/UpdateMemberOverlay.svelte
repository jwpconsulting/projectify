<script lang="ts">
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
</script>

<FilterMemberMenu {workspaceUserSearchModule} />
