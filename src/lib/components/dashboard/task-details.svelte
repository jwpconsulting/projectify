<script lang="ts">
    import {
        currenTaskDetailsUUID,
        currentWorkspaceUUID,
        deleteTask,
        newTaskSectionUUID,
        pushTashUUIDtoPath,
    } from "$lib/stores/dashboard";

    import {
        Query_DashboardTaskDetails,
        Mutation_AddTask,
        Mutation_UpdateTask,
        Mutation_AssignTask,
    } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";

    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import type { ReadableQuery } from "svelte-apollo";
    import { onDestroy } from "svelte";
    import ToolBar from "./toolBar.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import UserPicker from "../userPicker.svelte";
    import UserProfilePicture from "../userProfilePicture.svelte";
    import ProfilePicture from "../profilePicture.svelte";
    import TaskDetailsContent from "./task-details-content.svelte";
    import Tabs from "../tabs.svelte";
    import TaskDetailsDiscussion from "./task-details-discussion.svelte";
    import Tab from "../tab.svelte";
    import { goto } from "$app/navigation";
    import Loading from "../loading.svelte";

    let res: ReadableQuery<any> = null;
    let task = null;
    let subTasks = [];
    let labels = [];
    let taskModified = false;
    let isSaving = false;

    let taskWSStrore = null;

    function reset() {
        res = null;
        task = {
            title: "",
            description: "",
        };
        subTasks = [];
    }

    const refetch = debounce(() => {
        res?.refetch();
    }, 100);

    $: {
        if ($currenTaskDetailsUUID) {
            res = query(Query_DashboardTaskDetails, {
                variables: { uuid: $currenTaskDetailsUUID },
                fetchPolicy: "network-only",
            });
        } else {
            reset();
        }
    }

    $: {
        if (res && !$res.loading && $res.error) {
            goto("/error/task-not-found");
        }
    }

    $: {
        if ($currenTaskDetailsUUID) {
            taskWSStrore = getSubscriptionForCollection(
                "task",
                $currenTaskDetailsUUID
            );
        }
    }

    function setData(data) {
        if (!taskModified) {
            task = { ...data.task };
        }
    }

    let unsubscriber = null;
    $: {
        if (res && !$res.loading && !$res.error) {
            if (unsubscriber) {
                unsubscriber();
            }
            unsubscriber = res.subscribe(({ data }) => {
                if (!data) {
                    return;
                }
                setData(data);
            });
        }
    }

    onDestroy(() => {
        if (unsubscriber) {
            unsubscriber();
        }
    });

    $: {
        if ($taskWSStrore) {
            refetch();
        }
    }

    $: {
        if (res && $res.data) {
            subTasks = $res.data.task.subTasks.map((t) => {
                return {
                    ...t,
                    done: Boolean(t.done),
                };
            });

            labels = $res.data.task.labels;
        }
    }

    $: itsNew = $currenTaskDetailsUUID == null;

    $: saveEnabled = taskModified && task.title.length && !isSaving;

    async function save() {
        isSaving = true;

        const commonTaskInputs = {
            title: task.title,
            description: task.description,
            deadline: task.deadline || null,
        };

        if (itsNew) {
            let otherData: any = {};
            let assignee = task?.assignee?.email || null;

            if (assignee) {
                otherData.assignee = assignee;
            }

            if (labels) {
                otherData.labels = labels.map((l) => l.uuid);
            }

            if (subTasks) {
                otherData.subTasks = subTasks;
                otherData.subTasks = subTasks.map((s) => s.title);
            }

            try {
                let mRes = await client.mutate({
                    mutation: Mutation_AddTask,
                    variables: {
                        input: {
                            workspaceBoardSectionUuid: $newTaskSectionUUID,
                            ...commonTaskInputs,
                            ...otherData,
                        },
                    },
                });

                let taskUUID = mRes.data.addTask.uuid;
                currenTaskDetailsUUID.set(taskUUID);
                pushTashUUIDtoPath(taskUUID);
                taskModified = false;
            } catch (error) {
                console.error(error);
            }
        } else {
            try {
                let mRes = await client.mutate({
                    mutation: Mutation_UpdateTask,
                    variables: {
                        input: {
                            uuid: $currenTaskDetailsUUID,
                            ...commonTaskInputs,
                        },
                    },
                });
                taskModified = false;
            } catch (error) {
                console.error(error);
            }
        }

        await saveTaskAssignment();

        isSaving = false;
    }

    async function onDelete() {
        deleteTask(task, task.workspaceBoardSection.uuid);
    }

    let userPickerOpen = false;
    let userPicked = false;
    function onUserSelected({ detail: { user } }) {
        userPickerOpen = false;
        if (user?.email == task?.assignee?.email) {
            task.assignee = null;
        } else {
            task.assignee = user;
        }

        userPicked = true;

        saveTaskAssignment();
    }

    async function saveTaskAssignment() {
        if (!userPicked) {
            return;
        }
        if (!$currenTaskDetailsUUID) {
            return;
        }
        try {
            await client.mutate({
                mutation: Mutation_AssignTask,
                variables: {
                    input: {
                        uuid: $currenTaskDetailsUUID,
                        email: task?.assignee?.email || null,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
        userPicked = false;
    }

    $: tabItems = [
        {
            label: "Task",
            id: 1,
        },
        {
            label: "Discussion",
            hidden: itsNew,
            id: 2,
        },
    ];
</script>

{#if res && $res.loading}
    <div class="flex h-full w-[60vw] flex-col items-center justify-center p-0">
        <Loading />
    </div>
{:else if (res && !$res.error) || task}
    <div class="flex h-screen w-[60vw] flex-col p-0">
        <header class="relative flex items-center space-x-4 bg-base-100 p-6">
            <a
                href="/"
                class="flex items-center justify-center"
                on:click|preventDefault={() =>
                    (userPickerOpen = !userPickerOpen)}
            >
                {#if task?.assignee}
                    <UserProfilePicture
                        pictureProps={{
                            size: 42,
                            url: task.assignee.profilePicture,
                        }}
                    />
                {:else}
                    <ProfilePicture showPlus={true} size={42} />
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
                class="btn btn-primary btn-sm shrink-0 rounded-full"
                on:click={() => save()}>{$_("save")}</button
            >
            {#if userPickerOpen}
                <div class="absolute top-20 left-2 right-20 z-10 max-w-md">
                    <UserPicker
                        workspaceUUID={$currentWorkspaceUUID}
                        selectedUser={task.assignee}
                        on:userSelected={onUserSelected}
                    />
                </div>
            {/if}
        </header>

        <Tabs items={tabItems} autoPadding={false}>
            <Tab id={1}>
                <TaskDetailsContent
                    {task}
                    bind:subTasks
                    bind:labels
                    bind:taskModified
                />
            </Tab>
            <Tab id={2}>
                <TaskDetailsDiscussion {task} />
            </Tab>
        </Tabs>
    </div>
{/if}
