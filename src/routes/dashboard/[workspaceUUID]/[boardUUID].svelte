<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import Dashboard from "$lib/components/dashboard/dashboard.svelte";
</script>

<AuthGuard>
    <Dashboard />
</AuthGuard>
