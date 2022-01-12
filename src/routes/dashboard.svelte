<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import Workspaces from "$lib/components/dashboard/dashboard.svelte";
</script>

<AuthGuard>
    <Workspaces />
</AuthGuard>
