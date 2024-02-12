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
    import CreateWorkspaceBoard from "$lib/figma/overlays/constructive/CreateWorkspaceBoard.svelte";
    import CreateWorkspaceBoardSection from "$lib/figma/overlays/constructive/CreateWorkspaceBoardSection.svelte";
    import InviteWorkspaceUser from "$lib/figma/overlays/constructive/InviteWorkspaceUser.svelte";
    import RecoverWorkspaceBoard from "$lib/figma/overlays/constructive/RecoverWorkspaceBoard.svelte";
    import UpdateWorkspaceBoard from "$lib/figma/overlays/constructive/UpdateWorkspaceBoard.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    import UpdateWorkspaceBoardSection from "./UpdateWorkspaceBoardSection.svelte";

    export let target: ConstructiveOverlayType;
</script>

{#if target.kind === "updateWorkspaceBoard"}
    <UpdateWorkspaceBoard workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "createWorkspaceBoard"}
    <CreateWorkspaceBoard workspace={target.workspace} />
{:else if target.kind === "inviteWorkspaceUser"}
    <InviteWorkspaceUser workspace={target.workspace} />
{:else if target.kind === "createWorkspaceBoardSection"}
    <CreateWorkspaceBoardSection workspaceBoard={target.workspaceBoard} />
{:else if target.kind === "updateWorkspaceBoardSection"}
    <UpdateWorkspaceBoardSection
        workspaceBoardSection={target.workspaceBoardSection}
    />
{:else if target.kind === "recoverWorkspaceBoard"}
    <RecoverWorkspaceBoard workspaceBoard={target.workspaceBoard} />
{/if}
