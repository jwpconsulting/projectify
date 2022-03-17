<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import AuthGuard from "$lib/components/authGuard.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import Tabs from "$lib/components/tabs.svelte";
    import SettingsGeneral from "$lib/components/dashboard/settings-general.svelte";
    import TeamMembers from "$lib/components/dashboard/team-members.svelte";
    import { page } from "$app/stores";
    import SettingsLabels from "$lib/components/dashboard/settings-labels.svelte";

    $: workspaceUUID = $page.params["workspaceUUID"];

    $: tabItems = [
        {
            label: "General",
            id: 1,
            component: SettingsGeneral,
            props: { workspaceUUID },
        },
        {
            label: "Team members",
            id: 2,
            component: TeamMembers,
            props: { workspaceUUID },
        },
        {
            label: "Labels",
            id: 3,
            component: SettingsLabels,
            props: { workspaceUUID },
        },
    ];
</script>

<PageLayout>
    <AuthGuard>
        <SettingPage title="Workspace Settings">
            <Tabs items={tabItems} />
        </SettingPage>
    </AuthGuard>
</PageLayout>
