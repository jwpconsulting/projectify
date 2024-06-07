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
    import { _ } from "svelte-i18n";

    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Form from "$lib/figma/screens/task/Form.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import { createTask as createTaskFn } from "$lib/repository/workspace/task";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createTeamMemberAssignment } from "$lib/stores/dashboard/teamMemberAssignment";
    import {
        getDashboardSectionUrl,
        getDashboardProjectUrl,
        getNewTaskUrl,
        getTaskUrl,
    } from "$lib/urls";

    import type { PageData } from "./$types";
    import { beforeNavigate } from "$app/navigation";
    import type { BeforeNavigate } from "@sveltejs/kit";
    import type { FormViewState } from "$lib/types/ui";
    import { createSubTaskAssignment } from "$lib/stores/dashboard/subTaskAssignment";

    export let data: PageData;

    const { section } = data;
    $: project = section.project;

    // form fields
    let title: string | undefined = undefined;
    let description: string | null = null;
    let dueDate: string | null = null;

    // Do the following 3 variables have to be reactive? If so,
    // what do they depend on?
    const teamMemberAssignment = createTeamMemberAssignment();
    const labelAssignment = createLabelAssignment();
    const subTaskAssignment = createSubTaskAssignment();
    $: subTasks = subTaskAssignment.subTasks;

    $: canCreate =
        state.kind !== "done" &&
        state.kind !== "submitting" &&
        title !== undefined;

    type State = FormViewState | { kind: "done" };
    let state: State = { kind: "start" };

    async function action(continueEditing: boolean) {
        if (!title) {
            throw new Error("Expected title");
        }
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        const createTaskFull = {
            title,
            description,
            section: section,
            labels: $labelAssignment,
            assignee: $teamMemberAssignment ?? null,
            due_date: dueDate,
            sub_tasks: $subTasks ?? [],
        };
        state = { kind: "submitting" };
        try {
            const task = await createTaskFn(createTaskFull);
            if (continueEditing) {
                await goto(getTaskUrl(task));
                return;
            }
            state = { kind: "done" };
            await goto(getDashboardSectionUrl(section));
            return;
        } catch (e) {
            state = { kind: "error", message: JSON.stringify(e) };
            throw e;
        }
    }

    $: crumbs = [
        {
            label: project.title,
            href: getDashboardProjectUrl(project),
        },
        {
            label: section.title,
            href: getDashboardSectionUrl(section),
        },
        {
            label: $_("task-screen.new-task-breadcrumb"),
            href: getNewTaskUrl(section),
        },
    ];

    beforeNavigate((navigation: BeforeNavigate) => {
        if (state.kind === "done") {
            return;
        }
        const navigateAway = window.confirm(
            $_("task-screen.confirm-navigate-away.create"),
        );
        if (!navigateAway) {
            navigation.cancel();
        }
    });
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
            teamMemberAssignmentValidation={undefined}
            {labelAssignment}
            labelAssignmentValidation={undefined}
            {subTaskAssignment}
            subTaskAssignmentValidation={undefined}
            bind:title
            titleValidation={undefined}
            bind:dueDate
            dueDateValidation={undefined}
            bind:description
            descriptionValidation={undefined}
        />
    </svelte:fragment>
</Layout>
