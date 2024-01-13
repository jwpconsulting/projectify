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
    import { _, number } from "svelte-i18n";

    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Form from "$lib/figma/screens/task/Form.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import UpdateSubTasks from "$lib/figma/screens/task/UpdateSubTasks.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import { createSubTaskAssignment } from "$lib/stores/dashboard";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import type { TaskWithWorkspaceBoardSection } from "$lib/types/workspace";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskUrl,
    } from "$lib/urls";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { task } = data;
    const { workspace_board_section: workspaceBoardSection } = task;
    const { workspace_board: workspaceBoard } = workspaceBoardSection;

    // Initial data
    let { title, description } = task;
    let dueDate = task.due_date && coerceIsoDate(task.due_date);

    $: workspaceUserAssignment = createWorkspaceUserAssignment(task);
    $: labelAssignment = createLabelAssignment(task);
    $: subTaskAssignment = createSubTaskAssignment(task);
    $: subTasks = subTaskAssignment.subTasks;

    // XXX I am sure we can have really fancy validation
    $: canUpdate = !updating && title !== "" && $subTasks !== undefined;

    let updating = false;

    async function action(continueEditing: boolean) {
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        const submitTask: TaskWithWorkspaceBoardSection = {
            ...task,
            due_date: dueDate,
            title,
            description,
        };
        updating = true;
        try {
            await performUpdateTask(
                submitTask,
                {
                    title,
                    description,
                    due_date: dueDate,
                    assignee: $workspaceUserAssignment,
                    labels: $labelAssignment,
                    sub_tasks: $subTasks,
                    workspace_board_section: workspaceBoardSection,
                },
                { fetch },
            );
            if (continueEditing) {
                await goto(getTaskUrl(task.uuid));
                return;
            }
            await goto(
                getDashboardWorkspaceBoardSectionUrl(
                    workspaceBoardSection.uuid,
                ),
            );
        } catch (e) {
            updating = false;
            throw e;
        }
    }

    $: crumbs = [
        {
            label: workspaceBoard.title,
            href: getDashboardWorkspaceBoardUrl(workspaceBoard.uuid),
        },
        {
            label: workspaceBoardSection.title,
            href: getDashboardWorkspaceBoardSectionUrl(
                workspaceBoardSection.uuid,
            ),
        },
        // We could add a better task name here, or even
        // extract the whole thing as a layout for any task/[taskUuid] route
        { label: $number(task.number), href: getTaskUrl(task.uuid) },
    ];
</script>

<Layout>
    <TopBar slot="top-bar" {workspaceBoardSection}>
        <Breadcrumbs slot="breadcrumbs" {crumbs} />
        <svelte:fragment slot="buttons">
            <Button
                grow={false}
                action={{
                    kind: "submit",
                    form: "task-form",
                    disabled: !canUpdate,
                }}
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.update.update")}
            />
            <Button
                grow={false}
                action={{
                    kind: "button",
                    action: () => action(true),
                    disabled: !canUpdate,
                }}
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.update.update-continue-editing")}
            />
        </svelte:fragment>
    </TopBar>
    <svelte:fragment slot="content">
        <Form
            action={action.bind(null, false)}
            {workspaceUserAssignment}
            {labelAssignment}
            bind:title
            bind:dueDate
            bind:description
        />
        <UpdateSubTasks {subTaskAssignment} />
    </svelte:fragment>
</Layout>
