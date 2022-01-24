<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import Dashboard from "$lib/components/dashboard/dashboard.svelte";
    import { page } from "$app/stores";

    $: workspaceUUID = $page.params["workspaceUUID"];
    $: boardUUID = $page.params["boardUUID"];
</script>

<AuthGuard>
    <Dashboard
        selectedWorkspaceUUID={workspaceUUID}
        selectedBoardUUID={boardUUID}
    />
</AuthGuard>
