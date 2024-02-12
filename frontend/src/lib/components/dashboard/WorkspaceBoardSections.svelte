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

    import WorkspaceBoardSectionC from "$lib/figma/cards/WorkspaceBoardSection.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentWorkspaceBoardSections } from "$lib/stores/dashboard";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type {
        WorkspaceBoardSectionWithTasks,
        WorkspaceBoardDetail,
    } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoardDetail;

    let workspaceBoardSections: WorkspaceBoardSectionWithTasks[];
    $: workspaceBoardSections =
        $currentWorkspaceBoardSections ??
        workspaceBoard.workspace_board_sections;

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        });
    }
</script>

{#each workspaceBoardSections as workspaceBoardSection (workspaceBoardSection.uuid)}
    <WorkspaceBoardSectionC {workspaceBoard} {workspaceBoardSection} />
{:else}
    <section class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col">
        <p>
            {$_("dashboard.no-sections.message")}
        </p>
        <Button
            style={{ kind: "primary" }}
            color="blue"
            size="small"
            grow={false}
            label={$_("dashboard.no-sections.prompt")}
            action={{ kind: "button", action: onAddNewSection }}
        />
    </section>
{/each}
