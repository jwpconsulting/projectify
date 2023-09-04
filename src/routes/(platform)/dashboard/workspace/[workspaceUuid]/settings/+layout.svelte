<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getSettingsUrl } from "$lib/urls";

    import type { PageData } from "./$types";

    import { page } from "$app/stores";
    import SettingsPage from "$lib/components/SettingsPage.svelte";
    import TabsSimple from "$lib/components/tabs-simple.svelte";
    import type { TabItem } from "$lib/components/types";
    import { currentWorkspace } from "$lib/stores/dashboard";

    export let data: PageData;

    let { workspace } = data;

    $: workspace = $currentWorkspace ?? workspace;

    let activeTabId: string;

    let items: TabItem[] = [];
    $: {
        items = [
            {
                label: $_("settings.general"),
                id: "general",
                url: getSettingsUrl(workspace.uuid, "index"),
            },
            {
                label: $_("settings.labels"),
                id: "labels",
                url: getSettingsUrl(workspace.uuid, "labels"),
            },
            {
                label: $_("settings.team-members"),
                id: "team-members",
                url: getSettingsUrl(workspace.uuid, "team-members"),
            },
        ];
        const activeTab = items.find((item) => item.url == $page.url.pathname);
        if (activeTab) {
            activeTabId = activeTab.id;
        }
    }
</script>

<SettingsPage title={$_("workspace-settings")}>
    <TabsSimple {items} {activeTabId} />
    <main
        class="relative flex grow flex-col overflow-y-auto transition-all duration-300 ease-in-out"
    >
        <div class="relative flex grow flex-col px-4 py-4">
            <slot />
        </div>
    </main>
</SettingsPage>
