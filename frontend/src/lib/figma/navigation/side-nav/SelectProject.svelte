<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
    import { Folder } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { currentProject } from "$lib/stores/dashboard/project";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type {
        WorkspaceDetail,
        WorkspaceDetailProject,
    } from "$lib/types/workspace";
    import { getDashboardProjectUrl } from "$lib/urls";
    import { selectProjectUuid } from "$lib/stores/dashboard/ui";

    $: currentProjectUuid = $currentProject?.uuid;

    export let project: WorkspaceDetailProject;
    export let workspace: WorkspaceDetail;

    let buttonRef: HTMLElement;
    let contextMenuOpen = false;

    async function toggleMenu() {
        contextMenuOpen = true;
        // TODO: When the context menu is open, we should indicate that it
        // belongs to a certain board by highlighting the board in blue (using
        // the hover color)
        try {
            await openContextMenu(
                {
                    kind: "project",
                    workspace,
                    project,
                },
                buttonRef,
            );
        } finally {
            contextMenuOpen = false;
        }
    }
</script>

<a
    class="group block flex w-full flex-row justify-between gap-1 px-4 py-1 hover:bg-base-200"
    class:bg-base-200={contextMenuOpen}
    href={getDashboardProjectUrl(project)}
    on:click={() => selectProjectUuid(workspace.uuid, project.uuid)}
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <div
            class={`rounded-md p-1 ${
                project.uuid === currentProjectUuid ? "bg-primary-focus" : ""
            }`}
        >
            <Icon
                src={Folder}
                theme="outline"
                class={`h-4 w-4 ${
                    project.uuid === currentProjectUuid ? "text-base-100" : ""
                }`}
            />
        </div>
        <div class="line-clamp-1 min-w-0 font-bold">
            {project.title}
        </div>
    </div>
    {#if $currentTeamMemberCan("update", "project")}
        <div class="shrink-0" bind:this={buttonRef}>
            <CircleIcon
                size="medium"
                icon="ellipsis"
                action={{ kind: "button", action: toggleMenu }}
                ariaLabel={$_("dashboard.side-nav.projects.context-menu")}
            />
        </div>
    {/if}
</a>
