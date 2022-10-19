<script lang="ts">
    import WorkspaceSettingsBar from "$lib/figma/screens/workspace-settings/WorkspaceSettingsBar.svelte";
    import type { Workspace } from "$lib/types/workspace";
    import type { SettingKind } from "$lib/types/dashboard";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex w-[400px] flex-col gap-6 rounded-lg p-4 shadow-context-menu">
    <WorkspaceSettingsBar {workspace} {activeSetting} />
    <slot />
</div>
