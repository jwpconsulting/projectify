<script lang="ts">
    import { _ } from "svelte-i18n";

    import { getSettingsUrl } from "$lib/urls";

    import TabElement from "$lib/figma/buttons/TabElement.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex flex-row flex-wrap">
    <TabElement
        href={getSettingsUrl(workspace.uuid, "index")}
        label={$_("workspace-settings.tab-bar.general")}
        active={activeSetting === "index"}
    />
    <TabElement
        href={getSettingsUrl(workspace.uuid, "workspace-users")}
        label={$_("workspace-settings.tab-bar.workspace-users")}
        active={activeSetting === "workspace-users"}
    />
    <TabElement
        href={getSettingsUrl(workspace.uuid, "billing")}
        label={$_("workspace-settings.tab-bar.billing")}
        active={activeSetting === "billing"}
    />
    <div class="grow border-b-2 border-border" />
</div>
