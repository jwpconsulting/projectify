<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import SettingsPage from "$lib/components/SettingsPage.svelte";
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
    <SettingsPage title="Archives">
        <WorkspaceArchive />
    </SettingsPage>
</PageLayout>
