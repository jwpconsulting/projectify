<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import AuthGuard from "$lib/components/AuthGuard.svelte";
    import WorkspaceArchive from "$lib/components/dashboard/workspaceArchive.svelte";
    import { page } from "$app/stores";
    import { currentWorkspaceUuid } from "$lib/stores/dashboard";
    $: {
        const workspaceUuid = $page.params["workspaceUuid"];
        if (!workspaceUuid) {
            throw new Error("Expected workspaceUuid");
        }
        if (workspaceUuid != $currentWorkspaceUuid) {
            $currentWorkspaceUuid = workspaceUuid;
        }
    }
</script>

<PageLayout>
    <AuthGuard>
        <SettingPage title="Archives">
            <WorkspaceArchive />
        </SettingPage>
    </AuthGuard>
</PageLayout>
