<script lang="ts">
    import Board from "$lib/components/dashboard/board.svelte";
    import { page } from "$app/stores";

    import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";

    $: {
        $currentWorkspaceBoardUuid = $page.params["workspaceBoardUuid"];
        console.log($currentWorkspaceBoardUuid);
    }
</script>

<Board />
