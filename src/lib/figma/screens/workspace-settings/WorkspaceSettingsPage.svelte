<script lang="ts">
    import { _ } from "svelte-i18n";

    import WorkspaceSettingsTabBar from "$lib/figma/screens/workspace-settings/WorkspaceSettingsTabBar.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="max-w-xl w-full flex gap-4 flex-col">
    <h1 class="px-2 sm:px-0 text-2xl font-bold">
        {$_("workspace-settings.title")}
    </h1>
    <main
        class="w-full max-w-xl flex flex-col gap-6 rounded-lg p-4 shadow-context-menu bg-foreground"
    >
        <WorkspaceSettingsTabBar {workspace} {activeSetting} />
        <slot />
    </main>
</div>
