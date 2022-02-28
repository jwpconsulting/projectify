<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import AuthGuard from "$lib/components/authGuard.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import Tabs from "$lib/components/tabs.svelte";
    import SettingsGeneral from "$lib/components/dashboard/settings-general.svelte";
    import TeamMembers from "$lib/components/dashboard/team-members.svelte";

    const tabItems = [
        { label: "General", id: 1, component: SettingsGeneral },
        { label: "Team members", id: 2, component: TeamMembers },
    ];
</script>

<PageLayout>
    <AuthGuard>
        <SettingPage title="Workspace Settings">
            <Tabs items={tabItems} />
        </SettingPage>
    </AuthGuard>
</PageLayout>
