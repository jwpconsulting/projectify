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
<!--
@component
Up and down chevrons for task movement within a section
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import { moveTask, canMoveTask } from "$lib/repository/workspace/task";
    import type {
        SectionWithTasks,
        ProjectDetailTask,
    } from "$lib/types/workspace";
    import type { FormViewState } from "$lib/types/ui";
    import { getDashboardSectionUrl } from "$lib/urls";
    import { goto } from "$lib/navigation";
    import { getLogInWithNextUrl } from "$lib/urls/user";

    export let task: ProjectDetailTask;
    export let section: SectionWithTasks;

    let state: FormViewState = { kind: "start" };
    $: canMove =
        $currentTeamMemberCan("update", "task") && state.kind !== "submitting";

    async function move(where: "up" | "down") {
        state = { kind: "submitting" };
        const { error } = await moveTask(task, { kind: where, section });
        if (error?.code === 403) {
            await goto(getLogInWithNextUrl(getDashboardSectionUrl(section)));
            return;
        }
        if (error) {
            state = {
                kind: "error",
                message: $_("dashboard.task-card.move-error"),
            };
        } else {
            state = { kind: "start" };
        }
    }
</script>

<div
    class="flex flex-row items-center gap-1 {state.kind === 'error'
        ? 'rounded-xl border border-destructive'
        : ''}"
>
    {#if state.kind === "submitting"}
        {$_("dashboard.task-card.saving")}
    {:else}
        <CircleIcon
            size="medium"
            icon="up"
            action={{
                kind: "button",
                action: () => move("up"),
                disabled:
                    !canMoveTask(task, { kind: "up", section }) || !canMove,
            }}
            ariaLabel={$_("dashboard.task-card.move-up")}
        />
        <CircleIcon
            size="medium"
            icon="down"
            action={{
                kind: "button",
                action: () => move("down"),
                disabled:
                    !canMoveTask(task, { kind: "down", section }) || !canMove,
            }}
            ariaLabel={$_("dashboard.task-card.move-down")}
        />
    {/if}
</div>
