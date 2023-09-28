<script lang="ts">
    import { number } from "svelte-i18n";

    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
        getTaskUpdatesUrl,
    } from "$lib/urls";

    import type { PageData } from "../$types";

    import TaskUpdateBar from "$lib/figma/buttons/TaskUpdateBar.svelte";
    import Breadcrumbs from "$lib/figma/screens/task/Breadcrumbs.svelte";
    import Layout from "$lib/figma/screens/task/Layout.svelte";
    import TaskUpdates from "$lib/figma/screens/task/TaskUpdates.svelte";
    import TopBar from "$lib/figma/screens/task/TopBar.svelte";
    import type { TaskUpdateBarState } from "$lib/figma/types";
    import { currentTask } from "$lib/stores/dashboard";

    export let data: PageData;
    let { task } = data;
    const { workspaceBoardSection, workspaceBoard } = data;

    export let state: TaskUpdateBarState = "updates";

    $: task = $currentTask ?? task;

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
        { label: $number(task.number), href: getTaskUpdatesUrl(task.uuid) },
    ];
</script>

<Layout>
    <TopBar slot="top-bar" {workspaceBoardSection}>
        <Breadcrumbs slot="breadcrumbs" {crumbs} />
    </TopBar>
    <TaskUpdates slot="content" />
    <!-- TODO dry this up with the thing above -->
    <TaskUpdateBar slot="tab-bar-mobile" kind="mobile" {state} {task} />
</Layout>
