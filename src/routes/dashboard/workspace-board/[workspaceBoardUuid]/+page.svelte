<script lang="ts">
    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import { page } from "$app/stores";

    import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";

    $: {
        $currentWorkspaceBoardUuid = $page.params["workspaceBoardUuid"];
        console.log($currentWorkspaceBoardUuid);
    }
</script>

<Dashboard />
