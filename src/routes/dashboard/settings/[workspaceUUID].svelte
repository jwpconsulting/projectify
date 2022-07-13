<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import AuthGuard from "$lib/components/authGuard.svelte";
    import SettingPage from "$lib/components/settingPage.svelte";
    import Tabs from "$lib/components/tabs.svelte";
    import SettingsGeneral from "$lib/components/dashboard/settings-general.svelte";
    import TeamMembers from "$lib/components/dashboard/team-members.svelte";
    import { page } from "$app/stores";
    import SettingsLabels from "$lib/components/dashboard/settings-labels.svelte";
    import { _ } from "svelte-i18n";
    import { writable } from "svelte/store";
    import { goto } from "$app/navigation";
    import type { TabItem } from "$lib/components/types";

    $: workspaceUUID = $page.params["workspaceUUID"];

    $: tab = $page.url.searchParams.get("tab");
    $: activeTabId = writable(tab || "general");
    let items: TabItem[];
    $: items = [
        {
            label: $_("general"),
            id: "general",
            component: SettingsGeneral,
            props: { workspaceUUID },
        },
        {
            label: $_("members"),
            id: "members",
            component: TeamMembers,
            props: { workspaceUUID },
        },
        {
            label: $_("labels"),
            id: "labels",
            component: SettingsLabels,
            props: { workspaceUUID },
        },
    ];

    function onTabChanged({ detail: { tabId } }) {
        goto(`?tab=${tabId}`);
    }
</script>

<PageLayout>
    <AuthGuard>
        <SettingPage title={$_("workspace-settings")}>
            <Tabs {items} bind:activeTabId on:tabChanged={onTabChanged} />
        </SettingPage>
    </AuthGuard>
</PageLayout>
