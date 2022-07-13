<script lang="ts">
    import {
        assignUserToTask,
        currentTaskDetailsUUID,
        currentWorkspaceUUID,
        deleteTask,
        newTaskSectionUUID,
        pushTashUUIDtoPath,
    } from "$lib/stores/dashboard";

    import {
        Mutation_AddTask,
        Mutation_UpdateTask,
    } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import { getTask } from "$lib/repository";

    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
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
    import { page } from "$app/stores";
    import { writable } from "svelte/store";
    import IconClose from "../icons/icon-close.svelte";
    import TaskDetailsBreadcrumbs from "./task-details-breadcrumbs.svelte";
    import type { Task, SubTask, Label } from "$lib/types";
    import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";

    let task: Task | null = null;
    let loading = true;
    let failed = false;
    let subTasks: SubTask[] = [];
    let labels: Label[] = [];
    let taskModified = false;
    let isSaving = false;

    let taskWSStore: WSSubscriptionStore | null = null;

    $: uuids = $page.params["uuids"].split("/");
    $: activeTabId = writable(uuids[3] || "details");

    async function fetch() {
        if (!$currentTaskDetailsUUID) {
            throw new Error("Expected $currentTaskDetailsUUID");
        }
        try {
            task = await getTask($currentTaskDetailsUUID);
        } catch {
            failed = true;
        } finally {
            loading = false;
        }
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

    const refetch = debounce(() => {
        fetch();
    }, 100);

    $: {
        if ($currentTaskDetailsUUID) {
            fetch();
        } else {
            reset();
        }
    }

    $: {
        if (failed) {
            // TODO
            goto("/error/task-not-found");
        }
    }

    $: {
        if ($currentTaskDetailsUUID) {
            taskWSStore = getSubscriptionForCollection(
                "task",
                $currentTaskDetailsUUID
            );
        }
    }

    $: {
        if (taskWSStore) {
            refetch();
        }
    }

    $: {
        if (task) {
            subTasks = task.sub_tasks || [];
            labels = task.labels || [];
        }
    }

    let itsNew: boolean = false;
    $: itsNew = $currentTaskDetailsUUID == null;

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
            let otherData: any = {};
            let assignee = task?.assignee?.user.email || null;

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
                currentTaskDetailsUUID.set(taskUUID);
                pushTashUUIDtoPath(taskUUID);
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
                            uuid: $currentTaskDetailsUUID,
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
        if (!task) {
            throw new Error("Expected task");
        }
        deleteTask(task);
    }

    let userPickerOpen = false;
    let userPicked = false;
    function onUserSelected({ detail: { user } }) {
        if (!task) {
            throw new Error("Expected task");
        }
        userPickerOpen = false;
        if (user?.email == task?.assignee?.user.email) {
            task.assignee = undefined;
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
        if (!$currentTaskDetailsUUID) {
            return;
        }

        const userEmail = task?.assignee?.user.email;
        if (!userEmail) {
            throw new Error("Expected userEmail");
        }
        await assignUserToTask(userEmail, $currentTaskDetailsUUID);

        userPicked = false;
    }

    $: tabItems = [
        {
            label: $_("task"),
            id: "details",
        },
        {
            label: $_("updates"),
            hidden: itsNew,
            id: "updates",
        },
    ];

    import { getContext } from "svelte";
    const modal = getContext<any>("modal");
    function close() {
        modal.close();
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
                class="btn btn-circle btn-ghost h-[42px] min-h-[42px] w-[42px] min-w-[42px] shrink-0"
                ><IconClose /></button
            >
            <TaskDetailsBreadcrumbs {task} />
        </div>
        <header class="relative mb-2 flex items-center gap-4 bg-base-100 p-4">
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
                            url: task.assignee.user.profile_picture,
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
                class="btn btn-primary btn-md shrink-0"
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

        <Tabs bind:activeTabId items={tabItems} autoPadding={false}>
            <Tab id={"details"}>
                <TaskDetailsContent
                    {task}
                    bind:subTasks
                    bind:labels
                    bind:taskModified
                />
            </Tab>
            <Tab id={"updates"}>
                <TaskDetailsDiscussion {task} />
            </Tab>
        </Tabs>
    </div>
{/if}
