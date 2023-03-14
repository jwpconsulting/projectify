<script lang="ts">
    import {
        currentTask,
        currentTaskUuid,
        newTaskSectionUuid,
    } from "$lib/stores/dashboard";
    import { assignUserToTask, deleteTask } from "$lib/repository/workspace";

    import {
        Mutation_AddTask,
        Mutation_UpdateTask,
    } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";
    import ToolBar from "$lib/components/dashboard/toolBar.svelte";
    import IconTrash from "$lib/components/icons/icon-trash.svelte";
    import UserPicker from "$lib/components/userPicker.svelte";
    import UserProfilePicture from "$lib/components/userProfilePicture.svelte";
    import ProfilePicture from "$lib/components/profilePicture.svelte";
    import TaskDetailsContent from "$lib/components/dashboard/task-details-content.svelte";
    import Tabs from "$lib/components/tabs.svelte";
    import TaskDetailsDiscussion from "$lib/components/dashboard/task-details-discussion.svelte";
    import Tab from "$lib/components/tab.svelte";
    import { goto } from "$app/navigation";
    import Loading from "$lib/components/loading.svelte";
    import { page } from "$app/stores";
    import { writable } from "svelte/store";
    import IconClose from "$lib/components/icons/icon-close.svelte";
    import TaskDetailsBreadcrumbs from "$lib/components/dashboard/task-details-breadcrumbs.svelte";
    import type {
        Task,
        Label,
        SubTask,
        WorkspaceUser,
    } from "$lib/types/workspace";
    import { getDashboardTaskUrl } from "$lib/urls";

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

    let itsNew: boolean = false;
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
    function onUserSelected({
        detail: { user },
    }: {
        detail: { user: WorkspaceUser | null };
    }) {
        if (!task) {
            throw new Error("Expected task");
        }
        userPickerOpen = false;
        if (user?.user.email == task?.assignee?.user.email) {
            task.assignee = undefined;
        } else if (user) {
            task.assignee = user;
        } else {
            throw new Error("Expected user");
        }

        userPicked = true;

        saveTaskAssignment();
    }

    async function saveTaskAssignment() {
        if (!userPicked) {
            return;
        }
        if (!$currentTaskUuid) {
            return;
        }

        const userEmail = task?.assignee?.user.email;
        await assignUserToTask(userEmail ? userEmail : null, $currentTaskUuid);
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
                class="btn btn-ghost btn-circle h-[42px] min-h-[42px] w-[42px] min-w-[42px] shrink-0"
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
                        selectedUser={task.assignee}
                        on:userSelected={onUserSelected}
                    />
                </div>
            {/if}
        </header>

        <Tabs bind:activeTabId items={tabItems} autoPadding={false}>
            <Tab id={"details"}>
                <TaskDetailsContent bind:taskModified {task} />
            </Tab>
            <Tab id={"updates"}>
                <TaskDetailsDiscussion {task} />
            </Tab>
        </Tabs>
    </div>
{/if}
