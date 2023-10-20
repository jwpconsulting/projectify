<script lang="ts">
    import { _ } from "svelte-i18n";

    import TabElement from "$lib/figma/buttons/TabElement.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { Workspace } from "$lib/types/workspace";
    import { getSettingsUrl } from "$lib/urls";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex flex-row flex-wrap">
    <TabElement
        href={getSettingsUrl(workspace.uuid, "index")}
        label={$_("workspace-settings.general.title")}
        active={activeSetting === "index"}
    />
    <TabElement
        href={getSettingsUrl(workspace.uuid, "workspace-users")}
        label={$_("workspace-settings.workspace-users.title")}
        active={activeSetting === "workspace-users"}
    />
    <TabElement
        href={getSettingsUrl(workspace.uuid, "billing")}
        label={$_("workspace-settings.billing.title")}
        active={activeSetting === "billing"}
    />
    <div class="grow border-b-2 border-border" />
</div>
