<script lang="ts">
    import Fields from "$lib/figma/screens/task/Fields.svelte";
    import SubTaskBarComposite from "$lib/figma/screens/task/SubTaskBarComposite.svelte";
    import TaskDescription from "$lib/figma/screens/task/TaskDescription.svelte";
    import TaskDueDate from "$lib/figma/screens/task/TaskDueDate.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskSection from "$lib/figma/screens/task/TaskSection.svelte";
    import TaskTitle from "$lib/figma/screens/task/TaskTitle.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type {
        LabelAssignment,
        WorkspaceUserAssignment,
    } from "$lib/types/stores";
    import type {
        Label,
        SubTask,
        WorkspaceBoardSection,
        WorkspaceUser,
    } from "$lib/types/workspace";

    export let action: () => void;

    export let title: string | undefined;
    export let labels: Label[];
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let description: string | undefined;
    export let dueDate: string | undefined;
    export let assignedUser: WorkspaceUser | undefined;
    export let subTasks: SubTask[];

    export let workspaceUserAssignment: WorkspaceUserAssignment;
    export let labelAssignment: LabelAssignment;

    async function showUpdateWorkspaceUser(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateMember",
                workspaceUserAssignment,
            },
            anchor
        );
    }
    async function showUpdateLabel(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateLabel",
                labelAssignment,
            },
            anchor
        );
    }
</script>

<form on:submit|preventDefault={action}>
    <input type="submit" class="hidden" />
    <Fields>
        <TaskTitle slot="title" bind:title />
        <TaskUser
            slot="assignee"
            action={showUpdateWorkspaceUser}
            workspaceUser={assignedUser}
        />
        <TaskLabel slot="labels" action={showUpdateLabel} {labels} />
        <TaskSection slot="section" {workspaceBoardSection} />
        <TaskDueDate slot="due-date" bind:dueDate />
        <TaskDescription slot="description" bind:description />
    </Fields>
    <SubTaskBarComposite {subTasks} />
</form>
