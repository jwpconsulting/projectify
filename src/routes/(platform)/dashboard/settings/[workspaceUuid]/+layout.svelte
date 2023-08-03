<script lang="ts">
    import { _ } from "svelte-i18n";
    import SettingsPage from "$lib/components/SettingsPage.svelte";
    import { page } from "$app/stores";
    import TabsSimple from "$lib/components/tabs-simple.svelte";
    import type { TabItem } from "$lib/components/types";
    import Loading from "$lib/components/loading.svelte";
    import { currentWorkspace, loading } from "$lib/stores/dashboard";
    import { getSettingsUrl } from "$lib/urls";

    let activeTabId: string;

    let items: TabItem[] = [];
    $: {
        if ($currentWorkspace) {
            items = [
                {
                    label: $_("settings.general"),
                    id: "general",
                    url: getSettingsUrl($currentWorkspace.uuid, "index"),
                },
                {
                    label: $_("settings.labels"),
                    id: "labels",
                    url: getSettingsUrl($currentWorkspace.uuid, "labels"),
                },
                {
                    label: $_("settings.team-members"),
                    id: "team-members",
                    url: getSettingsUrl(
                        $currentWorkspace.uuid,
                        "team-members"
                    ),
                },
            ];
        }
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
            {#if $loading}
                <div class="flex min-h-[200px] items-center justify-center">
                    <Loading />
                </div>
            {/if}
            <div class:hidden={$loading}>
                <slot />
            </div>
        </div>
    </main>
</SettingsPage>
