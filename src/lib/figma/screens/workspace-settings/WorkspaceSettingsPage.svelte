<script lang="ts">
    import WorkspaceSettingsTabBar from "$lib/figma/screens/workspace-settings/WorkspaceSettingsTabBar.svelte";
    import type { Workspace } from "$lib/types/workspace";
    import type { SettingKind } from "$lib/types/dashboard";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex w-[400px] flex-col gap-6 rounded-lg p-4 shadow-context-menu">
    <WorkspaceSettingsTabBar {workspace} {activeSetting} />
    <slot />
</div>
