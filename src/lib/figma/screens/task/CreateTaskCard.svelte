<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getNewTaskUrl,
        getTaskUrl,
    } from "$lib/urls";

    import Breadcrumbs from "./Breadcrumbs.svelte";
    import Form from "./Form.svelte";

    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { createTask as createTaskFn } from "$lib/repository/workspace";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { createWorkspaceUserAssignment } from "$lib/stores/dashboard/workspaceUserAssignment";
    import type {
        CreateUpdateTask,
        SubTask,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { unwrap } from "$lib/utils/type";

    export let workspaceBoardSection: WorkspaceBoardSection;

    // form fields
    let title: string | undefined = undefined;
    let description: string | undefined = undefined;
    let dueDate: string | undefined = undefined;
    const subTasks: SubTask[] = [];

    const workspaceBoard = unwrap(
        workspaceBoardSection.workspace_board,
        "Expected workspaceBoard"
    );

    $: canCreate = title !== undefined;

    async function action(continueEditing: boolean) {
        if (!title) {
            throw new Error("Expected title and description");
        }
        const createTaskFull: CreateUpdateTask = {
            title,
            description,
            workspace_board_section: workspaceBoardSection,
            labels: $labelAssignment,
            assignee: $workspaceUserAssignment,
            deadline: dueDate,
        };
        const { uuid } = await createTaskFn(createTaskFull);
        if (continueEditing) {
            await goto(getTaskUrl(uuid));
            return;
        }
        await goto(
            getDashboardWorkspaceBoardSectionUrl(workspaceBoardSection.uuid)
        );
    }

    const workspaceUserAssignment = createWorkspaceUserAssignment();
    const labelAssignment = createLabelAssignment();

    $: crumbs = [
        {
            label: workspaceBoard.title,
            href: getDashboardWorkspaceBoardUrl(workspaceBoard.uuid),
        },
        {
            label: workspaceBoardSection.title,
            href: getDashboardWorkspaceBoardSectionUrl(
                workspaceBoardSection.uuid
            ),
        },
        {
            label: $_("task-screen.new-task-breadcrumb"),
            href: getNewTaskUrl(workspaceBoardSection.uuid),
        },
    ];
</script>

<Layout>
    <TopBar slot="top-bar" {workspaceBoardSection}>
        <Breadcrumbs slot="breadcrumbs" {crumbs} />
        <svelte:fragment slot="buttons">
            <Button
                action={{
                    kind: "submit",
                    form: "task-form",
                    disabled: !canCreate,
                }}
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.create.create")}
            />
            <Button
                action={{
                    kind: "button",
                    action: () => action(true),
                    disabled: !canCreate,
                }}
                color="blue"
                size="small"
                style={{ kind: "secondary" }}
                label={$_("task-screen.create.create-continue-editing")}
            />
        </svelte:fragment>
    </TopBar>

    <Form
        slot="content"
        action={action.bind(null, false)}
        {workspaceUserAssignment}
        {labelAssignment}
        bind:title
        bind:workspaceBoardSection
        bind:dueDate
        bind:description
        {subTasks}
    />
</Layout>
