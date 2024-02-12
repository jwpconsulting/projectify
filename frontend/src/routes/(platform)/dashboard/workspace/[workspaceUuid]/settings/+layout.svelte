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
    import Layout from "$lib/figma/screens/workspace-settings/Layout.svelte";
    import type { SettingKind } from "$lib/types/dashboard";

    import type { LayoutData } from "./$types";

    import { page } from "$app/stores";

    export let data: LayoutData;
    const { workspace } = data;

    function getActiveSetting({ pathname }: URL): SettingKind {
        if (pathname.endsWith("settings")) {
            return "index";
        } else if (pathname.endsWith("billing")) {
            return "billing";
        } else if (pathname.endsWith("workspace-users")) {
            return "workspace-users";
        }
        throw new Error("Unknown settings path");
    }

    $: settingKind = getActiveSetting($page.url);
</script>

<Layout {workspace} activeSetting={settingKind}>
    <slot />
</Layout>
