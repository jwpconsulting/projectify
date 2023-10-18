<script lang="ts">
    import type { PageData } from "./$types";

    import WorkspaceUsers from "$lib/figma/screens/workspace-settings/WorkspaceUsers.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard";

    export let data: PageData;

    let { workspace } = data;
    $: workspace = $currentWorkspace ?? workspace;
</script>

<WorkspaceUsers {workspace} />
