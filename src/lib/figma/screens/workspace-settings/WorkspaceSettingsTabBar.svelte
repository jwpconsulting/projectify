<script lang="ts">
    import { _ } from "svelte-i18n";
    import TabElement from "$lib/figma/buttons/TabElement.svelte";
    import { getSettingsUrl } from "$lib/urls";
    import type { Workspace } from "$lib/types/workspace";
    import type { SettingKind } from "$lib/types/dashboard";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex flex-row">
    <TabElement
        href={getSettingsUrl(workspace.uuid, "index")}
        label={$_("settings.general")}
        active={activeSetting === "index"}
    />
    <TabElement
        href={getSettingsUrl(workspace.uuid, "team-members")}
        label={$_("settings.members")}
        active={activeSetting === "team-members"}
    />
    <TabElement
        href={getSettingsUrl(workspace.uuid, "billing")}
        label={$_("settings.billing")}
        active={activeSetting === "billing"}
        grow={true}
    />
</div>
