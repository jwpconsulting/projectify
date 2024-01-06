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
    import WorkspaceBoardSections from "$lib/components/dashboard/WorkspaceBoardSections.svelte";
    import FloatingActionButton from "$lib/figma/buttons/FloatingActionButton.svelte";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceBoardDetail } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoardDetail;

    async function onAddNewSection() {
        await openConstructiveOverlay({
            kind: "createWorkspaceBoardSection",
            workspaceBoard,
        });
    }
</script>

<!-- Sections -->
<div class="flex flex-col gap-4 p-2">
    <WorkspaceBoardSections {workspaceBoard} />
</div>
<div class="self-end p-2">
    <FloatingActionButton icon="plus" action={onAddNewSection} />
</div>
