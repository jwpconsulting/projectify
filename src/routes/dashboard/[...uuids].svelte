<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import Dashboard from "$lib/components/dashboard/dashboard.svelte";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
</script>

<PageLayout footerVisible={false}>
    <AuthGuard>
        <Dashboard />
    </AuthGuard>
</PageLayout>
