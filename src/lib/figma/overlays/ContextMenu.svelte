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
    import HelpContextMenu from "$lib/figma/overlays/context-menu/HelpContextMenu.svelte";
    import Label from "$lib/figma/overlays/context-menu/Label.svelte";
    import Permissions from "$lib/figma/overlays/context-menu/Permissions.svelte";
    import Profile from "$lib/figma/overlays/context-menu/Profile.svelte";
    import SideNavContextMenu from "$lib/figma/overlays/context-menu/SideNavContextMenu.svelte";
    import Task from "$lib/figma/overlays/context-menu/Task.svelte";
    import Workspace from "$lib/figma/overlays/context-menu/Workspace.svelte";
    import WorkspaceBoard from "$lib/figma/overlays/context-menu/WorkspaceBoard.svelte";
    import WorkspaceBoardSection from "$lib/figma/overlays/context-menu/WorkspaceBoardSection.svelte";
    import WorkspaceUser from "$lib/figma/overlays/context-menu/WorkspaceUser.svelte";
    import type { ContextMenuType } from "$lib/types/ui";

    export let target: ContextMenuType;
</script>

{#if target.kind === "profile"}
    <Profile />
{:else if target.kind === "workspace"}
    <Workspace workspaces={target.workspaces} />
{:else if target.kind === "sideNav"}
    <SideNavContextMenu workspace={target.workspace} />
{:else if target.kind === "workspaceBoard"}
    <WorkspaceBoard
        workspace={target.workspace}
        workspaceBoard={target.workspaceBoard}
    />
{:else if target.kind === "workspaceBoardSection"}
    <WorkspaceBoardSection
        workspaceBoard={target.workspaceBoard}
        workspaceBoardSection={target.workspaceBoardSection}
    />
{:else if target.kind === "task"}
    <Task kind={target} />
{:else if target.kind === "help"}
    <HelpContextMenu />
{:else if target.kind === "permissions"}
    <Permissions />
{:else if target.kind === "updateWorkspaceUser"}
    <WorkspaceUser workspaceUserAssignment={target.workspaceUserAssignment} />
{:else if target.kind === "updateLabel"}
    <Label labelAssignment={target.labelAssignment} />
{/if}
