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
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import { updateTask as performUpdateTask } from "$lib/repository/workspace";
    import { createSubTaskAssignment } from "$lib/stores/dashboard";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createTeamMemberAssignment } from "$lib/stores/dashboard/teamMemberAssignment";
    import type { TaskWithSection } from "$lib/types/workspace";
    import {
        getDashboardSectionUrl,
        getDashboardProjectUrl,
        getTaskUrl,
    } from "$lib/urls";
    import { coerceIsoDate } from "$lib/utils/date";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { task } = data;
    const { section: section } = task;
    const { project: project } = section;

    // Initial data
    let { title, description } = task;
    let dueDate = task.due_date && coerceIsoDate(task.due_date);

    $: teamMemberAssignment = createTeamMemberAssignment(task);
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
        const submitTask: TaskWithSection = {
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
                    assignee: $teamMemberAssignment,
                    labels: $labelAssignment,
                    sub_tasks: $subTasks,
                    section: section,
                },
                { fetch },
            );
            if (continueEditing) {
                await goto(getTaskUrl(task.uuid));
                return;
            }
            await goto(getDashboardSectionUrl(section.uuid));
        } catch (e) {
            updating = false;
            throw e;
        }
    }

    $: crumbs = [
        {
            label: project.title,
            href: getDashboardProjectUrl(project.uuid),
        },
        {
            label: section.title,
            href: getDashboardSectionUrl(section.uuid),
        },
        // We could add a better task name here, or even
        // extract the whole thing as a layout for any task/[taskUuid] route
        { label: $number(task.number), href: getTaskUrl(task.uuid) },
    ];
</script>

<svelte:head>
    <title
        >{$_("task.update-task-title", {
            values: { title: task.title },
        })}</title
    >
</svelte:head>

<Layout>
    <TopBar slot="top-bar" {section}>
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
            {teamMemberAssignment}
            {labelAssignment}
            {subTaskAssignment}
            bind:title
            bind:dueDate
            bind:description
        />
    </svelte:fragment>
</Layout>
