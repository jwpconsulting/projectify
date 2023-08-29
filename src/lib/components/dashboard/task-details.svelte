<script lang="ts">
    /* eslint-disable */
    // TODO this file shall be deleted
    import { writable } from "svelte/store";
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import { getDashboardTaskUrl } from "$lib/urls";

    import { page } from "$app/stores";
    import TaskDetailsContent from "$lib/components/dashboard/task-details-content.svelte";
    import TaskDetailsDiscussion from "$lib/components/dashboard/task-details-discussion.svelte";
    import ToolBar from "$lib/components/dashboard/toolBar.svelte";
    import IconClose from "$lib/components/icons/icon-close.svelte";
    import IconTrash from "$lib/components/icons/icon-trash.svelte";
    import Loading from "$lib/components/loading.svelte";
    import { client } from "$lib/graphql/client";
    import {
        Mutation_AddTask,
        Mutation_UpdateTask,
    } from "$lib/graphql/operations";
    import { deleteTask } from "$lib/repository/workspace";
    import {
        currentTask,
        currentTaskUuid,
        newTaskSectionUuid,
        currentWorkspaceBoardUuid,
    } from "$lib/stores/dashboard";
    import type { Label, SubTask, Task } from "$lib/types/workspace";

    let task: Task | null = null;
    let loading = true;
    let failed = false;
    let subTasks: SubTask[] = [];
    let labels: Label[] = [];
    let taskModified = false;
    let isSaving = false;

    let activeTabId = writable<string>("details");
    $: {
        const tab = $page.url.searchParams.get("tab");
        $activeTabId = tab ? tab : "details";
    }

    function reset() {
        task = {
            title: "",
            description: "",
            _order: 0,
            uuid: "",
            number: 0,
            labels: [],
            created: "",
            modified: "",
        };
        subTasks = [];
    }

    $: {
        if (failed) {
            // TODO
            goto("/error/task-not-found");
        }
    }

    $: {
        if (!$currentTaskUuid) {
            reset();
            loading = false;
        }
    }

    $: {
        if ($currentTask) {
            task = $currentTask;
            subTasks = $currentTask.sub_tasks || [];
            labels = $currentTask.labels || [];
            loading = false;
        }
    }

    let itsNew = false;
    $: itsNew = $currentTaskUuid == null;

    $: saveEnabled = taskModified && task && task.title.length && !isSaving;

    async function save() {
        if (!task) {
            throw new Error("Expected task");
        }
        isSaving = true;

        const commonTaskInputs = {
            title: task.title,
            description: task.description,
            deadline: task.deadline || null,
        };

        if (itsNew) {
            let otherData: {
                assignee?: string;
                labels?: string[];
                subTasks?: string[];
            } = {};
            let assignee = task.assignee?.user.email || null;

            if (assignee) {
                otherData.assignee = assignee;
            }

            if (labels) {
                otherData.labels = labels.map((l) => l.uuid);
            }

            if (subTasks) {
                otherData.subTasks = subTasks.map((s) => s.title);
            }

            try {
                let mRes = await client.mutate({
                    mutation: Mutation_AddTask,
                    variables: {
                        input: {
                            workspaceBoardSectionUuid: $newTaskSectionUuid,
                            ...commonTaskInputs,
                            ...otherData,
                        },
                    },
                });

                let taskUuid = mRes.data.addTask.uuid;
                currentTaskUuid.set(taskUuid);
                if (!$currentWorkspaceBoardUuid) {
                    throw new Error("Expected $currentWorkspaceBoardUuid");
                }
                goto(
                    getDashboardTaskUrl(
                        $currentWorkspaceBoardUuid,
                        taskUuid,
                        "details"
                    )
                );
                taskModified = false;
            } catch (error) {
                console.error(error);
            }
        } else {
            try {
                await client.mutate({
                    mutation: Mutation_UpdateTask,
                    variables: {
                        input: {
                            uuid: $currentTaskUuid,
                            ...commonTaskInputs,
                        },
                    },
                });
                taskModified = false;
            } catch (error) {
                console.error(error);
            }
        }

        isSaving = false;
    }

    async function onDelete() {
        if (!task) {
            throw new Error("Expected task");
        }
        deleteTask(task);
    }
</script>

{#if loading}
    <div class="flex h-full w-[60vw] flex-col items-center justify-center p-0">
        <Loading />
    </div>
{:else if task}
    <div class="flex h-screen w-[60vw] flex-col p-0">
        <div class="flex items-center gap-4 px-4 py-4 pb-2">
            <button
                on:click={() => close()}
                class="btn btn-ghost btn-circle h-[42px] min-h-[42px] w-[42px] min-w-[42px] shrink-0"
                ><IconClose /></button
            >
        </div>
        <header class="relative mb-2 flex items-center gap-4 bg-base-100 p-4">
            <a href="/" class="flex items-center justify-center">
                {#if task.assignee}
                    TODO: A user profile picture may be shown here
                {:else}
                    TODO: A profile picture may be shown here
                {/if}
            </a>

            <input
                class="nowrap-ellipsis input grow rounded-md p-2 text-xl"
                placeholder={$_("task-name")}
                on:keydown={(e) => {
                    if (e.key == "Enter") {
                        e.preventDefault();
                        save();
                    }
                }}
                on:input={() => (taskModified = true)}
                bind:value={task.title}
            />

            <ToolBar
                items={[
                    {
                        label: $_("Delete"),
                        icon: IconTrash,
                        onClick: onDelete,
                        hidden: itsNew,
                    },
                ]}
            />

            <button
                disabled={!saveEnabled}
                class="btn btn-primary btn-md shrink-0"
                on:click={() => save()}>{$_("save")}</button
            >
        </header>

        <TaskDetailsContent {task} />
        <TaskDetailsDiscussion {task} />
    </div>
{/if}
