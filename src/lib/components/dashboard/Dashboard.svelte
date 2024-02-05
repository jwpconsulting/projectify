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

    import WorkspaceBoardSections from "$lib/components/dashboard/WorkspaceBoardSections.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoardDetail } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoardDetail;

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        });
    }

    $: hasSections = workspaceBoard.workspace_board_sections.length > 0;
</script>

<!-- Sections -->
<div class="flex flex-col gap-4 p-2">
    <WorkspaceBoardSections {workspaceBoard} />
</div>

{#if hasSections}
    <div class="sticky bottom-0 self-end p-2">
        <Button
            style={{ kind: "primary" }}
            label={$_("dashboard.actions.add-workspace-board-section")}
            size="medium"
            action={{ kind: "button", action: onAddNewSection }}
            color="blue"
        />
    </div>
{/if}
