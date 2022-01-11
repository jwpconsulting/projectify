<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import Workspaces from "$lib/components/tasks/workspaces.svelte";
</script>

<AuthGuard>
    <Workspaces />
</AuthGuard>
