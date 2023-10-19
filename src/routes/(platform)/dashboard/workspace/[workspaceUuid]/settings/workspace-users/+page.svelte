<script lang="ts">
    import WorkspaceUsers from "$lib/figma/screens/workspace-settings/WorkspaceUsers.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard";

    import type { PageData } from "./$types";

    export let data: PageData;

    let { workspace } = data;
    $: workspace = $currentWorkspace ?? workspace;
</script>

<WorkspaceUsers {workspace} />
