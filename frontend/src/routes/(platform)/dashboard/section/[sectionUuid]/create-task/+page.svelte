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

    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Form from "$lib/figma/screens/task/Form.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import {
        createTask as createTaskFn,
        type CreateUpdateTaskData,
    } from "$lib/repository/workspace";
    import { createSubTaskAssignment } from "$lib/stores/dashboard";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createTeamMemberAssignment } from "$lib/stores/dashboard/teamMemberAssignment";
    import {
        getDashboardSectionUrl,
        getDashboardProjectUrl,
        getNewTaskUrl,
        getTaskUrl,
    } from "$lib/urls";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { section } = data;
    $: project = section.project;

    // form fields
    let title: string | undefined = undefined;
    let description: string | undefined = undefined;
    let dueDate: string | undefined = undefined;

    // Do the following 3 variables have to be reactive? If so,
    // what do they depend on?
    const teamMemberAssignment = createTeamMemberAssignment();
    const labelAssignment = createLabelAssignment();
    const subTaskAssignment = createSubTaskAssignment();
    $: subTasks = subTaskAssignment.subTasks;

    $: canCreate = !creating && title !== undefined;

    let creating = false;

    async function action(continueEditing: boolean) {
        if (!title) {
            throw new Error("Expected title");
        }
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        const createTaskFull: CreateUpdateTaskData = {
            title,
            description,
            section: section,
            labels: $labelAssignment,
            assignee: $teamMemberAssignment,
            due_date: dueDate,
            sub_tasks: $subTasks,
        };
        creating = true;
        try {
            const { uuid } = await createTaskFn(createTaskFull, { fetch });
            if (continueEditing) {
                await goto(getTaskUrl(uuid));
                return;
            }
            await goto(getDashboardSectionUrl(section.uuid));
            return;
        } catch (e) {
            creating = false;
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
        {
            label: $_("task-screen.new-task-breadcrumb"),
            href: getNewTaskUrl(section.uuid),
        },
    ];
</script>

<svelte:head>
    <title
        >{$_("task.create-task-title", {
            values: { title: project.title },
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
                    disabled: !canCreate,
                }}
                color="blue"
                size="medium"
                style={{ kind: "primary" }}
                label={$_("task-screen.create.create")}
            />
            <Button
                grow={false}
                action={{
                    kind: "button",
                    action: () => action(true),
                    disabled: !canCreate,
                }}
                color="blue"
                size="medium"
                style={{ kind: "secondary" }}
                label={$_("task-screen.create.create-continue-editing")}
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
