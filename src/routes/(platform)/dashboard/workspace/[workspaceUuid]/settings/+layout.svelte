<script lang="ts">
    import type { LayoutData } from "./$types";

    import { page } from "$app/stores";
    import Layout from "$lib/figma/screens/workspace-settings/Layout.svelte";
    import type { SettingKind } from "$lib/types/dashboard";

    export let data: LayoutData;
    const { workspace } = data;

    function getActiveSetting({ pathname }: URL): SettingKind {
        if (pathname.endsWith("settings")) {
            return "index";
        } else if (pathname.endsWith("billing")) {
            return "billing";
        } else if (pathname.endsWith("team-members")) {
            return "team-members";
        }
        throw new Error("Unknown settings path");
    }

    $: settingKind = getActiveSetting($page.url);
</script>

<div class="flex h-full flex-col items-center bg-background px-0 py-8 sm:px-2">
    <Layout {workspace} activeSetting={settingKind}>
        <slot />
    </Layout>
</div>
