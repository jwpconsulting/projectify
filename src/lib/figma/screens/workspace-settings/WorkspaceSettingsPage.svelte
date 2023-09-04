<script lang="ts">
    import WorkspaceSettingsTabBar from "$lib/figma/screens/workspace-settings/WorkspaceSettingsTabBar.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div
    class="flex w-[400px] flex-col gap-6 rounded-lg p-4 shadow-context-menu bg-foreground"
>
    <WorkspaceSettingsTabBar {workspace} {activeSetting} />
    <slot />
</div>
