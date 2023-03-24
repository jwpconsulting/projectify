<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
</script>

<PageLayout footerVisible={false} heightScreen={true}>
    <AuthGuard>
        <Dashboard />
    </AuthGuard>
</PageLayout>
