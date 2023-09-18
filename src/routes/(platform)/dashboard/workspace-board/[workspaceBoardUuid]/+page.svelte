<script lang="ts">
    import type { PageData } from "./$types";

    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import { currentWorkspaceBoard } from "$lib/stores/dashboard";

    export let data: PageData;

    let { workspaceBoard } = data;

    $: workspaceBoard = $currentWorkspaceBoard ?? workspaceBoard;
</script>

<Dashboard {workspaceBoard} />
