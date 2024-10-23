<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Form from "$lib/figma/screens/task/Form.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { goto } from "$lib/navigation";
    import { createTask } from "$lib/repository/workspace/task";
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
    import { toValid, type InputFieldValidation } from "$lib/funabashi/types";
    import { persisted } from "svelte-local-storage-store";

    export let data: PageData;

    const { section } = data;
    $: project = section.project;

    // form fields
    const titleInput = persisted<string | null>("create-task-title", null);
    let titleValidation: InputFieldValidation | undefined = undefined;
    let description: string | null = null;
    let descriptionValidation: string | undefined = undefined;
    let dueDate: string | null = null;
    let dueDateValidation: InputFieldValidation | undefined = undefined;

    // Do the following 3 variables have to be reactive? If so,
    // what do they depend on?
    const teamMemberAssignment = createTeamMemberAssignment();
    let teamMemberAssignmentValidation: string | undefined = undefined;
    const labelAssignment = createLabelAssignment();
    let labelAssignmentValidation: string | undefined = undefined;
    const subTaskAssignment = createSubTaskAssignment();
    let subTaskAssignmentValidation: string | undefined = undefined;
    $: subTasks = subTaskAssignment.subTasks;

    $: canCreate =
        state.kind !== "done" &&
        state.kind !== "submitting" &&
        $titleInput !== null;

    type State = FormViewState | { kind: "done" };
    let state: State = { kind: "start" };

    function hasInputSomething() {
        const conditions: boolean[] = [
            $titleInput !== null,
            description !== null,
            dueDate !== null,
            $teamMemberAssignment !== null,
            $labelAssignment.length > 0,
            $subTasks.length > 0,
        ];
        return conditions.some((a) => a);
    }

    function resetForm() {
        $titleInput = null;
    }

    async function action(continueEditing: boolean) {
        if (!$titleInput) {
            throw new Error("Expected title");
        }
        state = { kind: "submitting" };
        const { error, data } = await createTask({
            title: $titleInput,
            description,
            section: section,
            labels: $labelAssignment,
            assignee: $teamMemberAssignment,
            due_date: dueDate,
            sub_tasks: $subTasks,
        });
        if (data) {
            state = { kind: "done" };
            if (continueEditing) {
                await goto(getTaskUrl(data));
                return;
            }
            await goto(getDashboardSectionUrl(section));
            resetForm();
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("task-screen.create.errors.server", {
                    values: { error: JSON.stringify(error) },
                }),
            };
            return;
        }
        if (error.code === 403) {
            state = {
                kind: "error",
                message: $_("task-screen.create.errors.authentication"),
            };
            return;
        }
        state = {
            kind: "error",
            message: $_("task-screen.create.errors.field"),
        };
        // TODO
        const { details } = error;
        titleValidation = toValid(
            details.title,
            $_("task-screen.form.title.valid"),
        );
        dueDateValidation = toValid(
            details.due_date,
            $_("task-screen.form.due-date.valid"),
        );
        descriptionValidation = details.description;
        subTaskAssignmentValidation = details.sub_tasks
            ? `TODO: ${JSON.stringify(details.sub_tasks)}`
            : undefined;
        labelAssignmentValidation = details.labels
            ? `TODO: ${JSON.stringify(details.labels)}`
            : undefined;
        teamMemberAssignmentValidation = details.assignee
            ? `TODO: ${JSON.stringify(details.assignee)}`
            : undefined;
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
        if (!hasInputSomething()) {
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
        {#if state.kind === "error"}
            <p>{state.message}</p>
        {/if}
        <Form
            action={action.bind(null, false)}
            {teamMemberAssignment}
            {teamMemberAssignmentValidation}
            {labelAssignment}
            {labelAssignmentValidation}
            {subTaskAssignment}
            {subTaskAssignmentValidation}
            bind:title={$titleInput}
            {titleValidation}
            bind:dueDate
            {dueDateValidation}
            bind:description
            {descriptionValidation}
        />
    </svelte:fragment>
</Layout>
