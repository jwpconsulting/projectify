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
    import { Briefcase } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { selectWorkspaceUuid } from "$lib/stores/dashboard/ui";
    import type { WorkspaceDetail } from "$lib/types/workspace";
    import { getDashboardWorkspaceUrl } from "$lib/urls";

    export let workspaces: Pick<WorkspaceDetail, "title" | "uuid">[];
</script>

<Layout>
    <p class="px-4 py-2 font-bold">
        {$_("overlay.context-menu.workspace.select-workspace")}
    </p>
    {#each workspaces as workspace}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getDashboardWorkspaceUrl(workspace),
                onInteract: () => selectWorkspaceUuid(workspace.uuid),
            }}
            label={workspace.title}
            icon={Briefcase}
        />
    {/each}
</Layout>
