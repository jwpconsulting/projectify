<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getNewTaskUrl,
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
        Label,
        SubTask,
        WorkspaceBoardSection,
        WorkspaceUser,
    } from "$lib/types/workspace";
    import { unwrap } from "$lib/utils/type";

    export let workspaceBoardSection: WorkspaceBoardSection;

    // form fields
    let title: string | undefined = undefined;
    let description: string | undefined = undefined;
    let assignedUser: WorkspaceUser | undefined = undefined;
    let labels: Label[] = [];
    let dueDate: string | undefined = undefined;
    const subTasks: SubTask[] = [];

    const workspaceBoard = unwrap(
        workspaceBoardSection.workspace_board,
        "Expected workspaceBoard"
    );

    // TODO add me back:
    // const labelAssignment = createLabelAssignment();

    $: canCreate = title !== undefined && description !== undefined;

    async function action() {
        if (!title || !description) {
            throw new Error("Expected title and description");
        }
        const createTaskFull: CreateUpdateTask = {
            title,
            description,
            workspace_board_section: workspaceBoardSection,
            labels,
            assignee: assignedUser,
            deadline: dueDate,
        };
        await createTaskFn(createTaskFull);
        // TODO allow player to keep editing this task
        // Like django admin's save then continue editing
        await goto(
            getDashboardWorkspaceBoardSectionUrl(workspaceBoardSection.uuid)
        );
    }

    const workspaceUserAssignment = createWorkspaceUserAssignment();
    const labelAssignment = createLabelAssignment();

    $: assignedUser = $workspaceUserAssignment;
    $: labels = $labelAssignment;

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
        <Button
            slot="buttons"
            action={{
                kind: "button",
                action,
                disabled: !canCreate,
            }}
            color="blue"
            size="small"
            style={{ kind: "primary" }}
            label={$_("task-screen.save")}
        />
    </TopBar>

    <Form
        slot="content"
        {action}
        {workspaceUserAssignment}
        {labelAssignment}
        bind:title
        bind:assignedUser
        bind:labels
        bind:workspaceBoardSection
        bind:dueDate
        bind:description
        {subTasks}
    />
</Layout>
