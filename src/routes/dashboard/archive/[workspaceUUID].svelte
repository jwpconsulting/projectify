<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import AuthGuard from "$lib/components/authGuard.svelte";
    import WorkspaceArchive from "$lib/components/dashboard/workspaceArchive.svelte";
</script>

<PageLayout>
    <AuthGuard>
        <SettingPage title="Archives">
            <WorkspaceArchive />
        </SettingPage>
    </AuthGuard>
</PageLayout>
