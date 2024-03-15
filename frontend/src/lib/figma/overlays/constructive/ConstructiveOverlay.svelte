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
    import CreateProject from "$lib/figma/overlays/constructive/CreateProject.svelte";
    import CreateSection from "$lib/figma/overlays/constructive/CreateSection.svelte";
    import InviteWorkspaceUser from "$lib/figma/overlays/constructive/InviteWorkspaceUser.svelte";
    import RecoverProject from "$lib/figma/overlays/constructive/RecoverProject.svelte";
    import UpdateProject from "$lib/figma/overlays/constructive/UpdateProject.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    import UpdateSection from "./UpdateSection.svelte";

    export let target: ConstructiveOverlayType;
</script>

{#if target.kind === "updateProject"}
    <UpdateProject project={target.project} />
{:else if target.kind === "createProject"}
    <CreateProject workspace={target.workspace} />
{:else if target.kind === "inviteWorkspaceUser"}
    <InviteWorkspaceUser workspace={target.workspace} />
{:else if target.kind === "createSection"}
    <CreateSection project={target.project} />
{:else if target.kind === "updateSection"}
    <UpdateSection section={target.section} />
{:else if target.kind === "recoverProject"}
    <RecoverProject project={target.project} />
{/if}
