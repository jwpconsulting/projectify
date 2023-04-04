<script lang="ts">
    import Loading from "$lib/components/loading.svelte";
    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import { page } from "$app/stores";

    import {
        currentWorkspaceBoard,
        currentWorkspaceBoardUuid,
    } from "$lib/stores/dashboard";

    $: {
        $currentWorkspaceBoardUuid = $page.params["workspaceBoardUuid"];
        console.log($currentWorkspaceBoardUuid);
    }
</script>

{#if $currentWorkspaceBoard}
    <Dashboard workspaceBoard={$currentWorkspaceBoard} />
{:else}
    <Loading />
{/if}
