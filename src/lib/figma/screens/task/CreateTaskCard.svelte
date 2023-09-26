<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getNewTaskUrl,
    } from "$lib/urls";

    import Breadcrumbs from "./Breadcrumbs.svelte";

    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskFieldsTemplate from "$lib/figma/screens/task/TaskFieldsTemplate.svelte";
    import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { createTask as createTaskFn } from "$lib/repository/workspace";
    import type {
        CreateTask,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { unwrap } from "$lib/utils/type";

    export let workspaceBoardSection: WorkspaceBoardSection;

    // form fields
    let title: string | undefined = undefined;
    let description: string | undefined = undefined;

    const workspaceBoard = unwrap(
        workspaceBoardSection.workspace_board,
        "Expected workspaceBoard"
    );

    // TODO add me back:
    // const labelAssignment = createLabelAssignment();

    $: canCreate = title !== undefined && description !== undefined;

    async function createTask() {
        if (!title || !description) {
            throw new Error("Expected title and description");
        }
        const createTaskFull: CreateTask = {
            title,
            description,
            workspace_board_section: workspaceBoardSection,
            // TODO
            labels: [],
            // TODO
            deadline: null,
        };
        await createTaskFn(createTaskFull);
        // TODO allow player to keep editing this task
        // Like django admin's save then continue editing
        await goto(
            getDashboardWorkspaceBoardSectionUrl(workspaceBoardSection.uuid)
        );
    }

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
                action: createTask,
                disabled: !canCreate,
            }}
            color="blue"
            size="small"
            style={{ kind: "primary" }}
            label={$_("task-screen.save")}
        />
    </TopBar>

    <TaskFieldsTemplate slot="content">
        <TaskTitle slot="title" bind:title />
        <TaskSection slot="section" {workspaceBoardSection} />
        <TaskDescription slot="description" bind:description />
    </TaskFieldsTemplate>
</Layout>
