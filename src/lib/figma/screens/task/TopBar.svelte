<script lang="ts">
    import { _ } from "svelte-i18n";

    import {
        getDashboardWorkspaceBoardSectionUrl,
        getDashboardWorkspaceBoardUrl,
    } from "$lib/urls";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { CreateOrUpdateTaskModule } from "$lib/types/stores";
    import type {
        TaskOrNewTask,
        BreadCrumbTask,
        ContextMenuType,
    } from "$lib/types/ui";
    import {
        isBreadCrumbWorkspaceBoardSection,
        isBreadCrumbTask,
    } from "$lib/types/ui";

    export let taskModule: CreateOrUpdateTaskModule | null;
    // TODO Can we pull this out of taskModule too? Justus 2023-05-08
    export let taskOrNewTask: TaskOrNewTask;

    export let editLink: string | null = null;

    const canCreateOrUpdate = taskModule ? taskModule.canCreateOrUpdate : null;

    let contextMenuRef: HTMLElement;
    let contextMenuType: ContextMenuType | undefined;
    let breadCrumbTask: BreadCrumbTask;
    $: {
        if (taskOrNewTask.kind === "task") {
            const { task } = taskOrNewTask;
            const { workspace_board_section: workspaceBoardSection } = task;
            if (!workspaceBoardSection) {
                throw new Error("Expected workspaceBoardSection");
            }
            if (!isBreadCrumbTask(task)) {
                throw new Error(`Failed to crumble task ${task.uuid}'s bread`);
            }
            breadCrumbTask = task;
            contextMenuType = {
                kind: "task",
                task: taskOrNewTask.task,
                location: "task",
                moveTaskModule: undefined,
                workspaceBoardSection,
            };
        } else {
            const { newTask } = taskOrNewTask;
            const { workspace_board_section } = newTask;
            if (!isBreadCrumbWorkspaceBoardSection(workspace_board_section)) {
                throw new Error(
                    `Failed to crumble workspace board section ${workspace_board_section.uuid}'s bread`
                );
            }
            breadCrumbTask = {
                workspace_board_section,
            };
        }
    }

    const createOrUpdate = taskModule ? taskModule.createOrUpdateTask : null;

    $: workspaceBoardUrl = getDashboardWorkspaceBoardUrl(
        breadCrumbTask.workspace_board_section.workspace_board.uuid
    );
    $: workspaceBoardSectionUrl = getDashboardWorkspaceBoardSectionUrl(
        breadCrumbTask.workspace_board_section.uuid
    );
</script>

<div class="flex flex-row items-center justify-between">
    <div class="flex flex-row items-center gap-6">
        <div class="shrink-0">
            <CircleIcon
                action={{
                    kind: "a",
                    href: workspaceBoardSectionUrl,
                }}
                size="medium"
                icon="close"
            />
        </div>
        <div class="text-sm font-bold text-utility">
            <Anchor
                label={breadCrumbTask.workspace_board_section.workspace_board
                    .title}
                size="small"
                href={workspaceBoardUrl}
            /> &gt;
            <Anchor
                label={breadCrumbTask.workspace_board_section.title}
                size="small"
                href={workspaceBoardSectionUrl}
            />
            {#if breadCrumbTask.number}&gt; {breadCrumbTask.number}{/if}
        </div>
    </div>
    <div class="flex h-10 flex-row items-center gap-4">
        {#if editLink}
            <Button
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.edit")}
                action={{ kind: "a", href: editLink }}
            />
        {/if}
        {#if createOrUpdate}
            <Button
                action={{
                    kind: "button",
                    action: createOrUpdate,
                    disabled: !$canCreateOrUpdate,
                }}
                color="blue"
                size="small"
                style={{ kind: "primary" }}
                label={$_("task-screen.save")}
            />
        {/if}
        <div bind:this={contextMenuRef}>
            {#if contextMenuType}
                <SquovalIcon
                    icon="dotsVertical"
                    state="active"
                    action={{
                        kind: "button",
                        action: openContextMenu.bind(
                            null,
                            contextMenuType,
                            contextMenuRef
                        ),
                    }}
                />
            {/if}
        </div>
    </div>
</div>
