<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
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
