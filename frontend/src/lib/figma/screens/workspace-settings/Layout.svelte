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

    import TabBar from "$lib/figma/screens/workspace-settings/TabBar.svelte";
    import type { SettingKind } from "$lib/types/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    export let activeSetting: SettingKind;
</script>

<div class="flex w-full max-w-xl flex-col gap-4">
    <h1 class="px-2 text-2xl font-bold sm:px-0">
        {$_("workspace-settings.title")}
    </h1>
    <main
        class="flex w-full max-w-xl flex-col gap-6 rounded-lg bg-foreground p-4 shadow-context-menu"
    >
        <TabBar {workspace} {activeSetting} />
        <slot />
    </main>
</div>
