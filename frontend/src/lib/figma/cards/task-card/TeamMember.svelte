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
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { createTeamMemberAssignment } from "$lib/stores/dashboard/teamMemberAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { TaskWithSection } from "$lib/types/workspace";

    export let task: TaskWithSection;

    let userPickerBtnRef: HTMLElement;

    $: teamMemberAssignment = createTeamMemberAssignment(task);

    $: assignee = $teamMemberAssignment;

    async function openUserPicker() {
        const contextMenuType: ContextMenuType = {
            kind: "updateTeamMember",
            teamMemberAssignment,
        };
        await openContextMenu(contextMenuType, userPickerBtnRef);
        const teamMember = $teamMemberAssignment;
        // XXX need to investigate what happens when sub tasks change while
        // the user picker is open. Possibly, a sub task can be deleted if
        // it is added
        await updateTask(
            task,
            { ...task, assignee: teamMember },
            {
                fetch,
            },
        );
    }

    $: canUpdate = $currentTeamMemberCan("update", "task");
</script>

<button
    bind:this={userPickerBtnRef}
    on:click|preventDefault={canUpdate ? openUserPicker : undefined}
>
    <AvatarVariant
        content={{ kind: "single", user: assignee?.user }}
        size="medium"
    />
</button>
