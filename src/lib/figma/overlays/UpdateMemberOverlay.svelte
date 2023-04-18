<script lang="ts">
    import type { WorkspaceUserSearchModule } from "$lib/types/stores";
    import FilterMemberMenu from "$lib/figma/composites/FilterMemberMenu.svelte";

    export let workspaceUserSearchModule: WorkspaceUserSearchModule;
</script>

<FilterMemberMenu {workspaceUserSearchModule} />
