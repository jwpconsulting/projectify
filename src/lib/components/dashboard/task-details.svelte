<script lang="ts">
    import {
        closeTaskDetails,
        currenTaskDetailsUUID,
        currentWorkspaceUUID,
        newTaskSectionUUID,
        pushTashUUIDtoPath,
    } from "$lib/stores/dashboard";
    import IconPlus from "../icons/icon-plus.svelte";

    import {
        Query_DashboardTaskDetails,
        Mutation_AddTask,
        Mutation_UpdateTask,
        Mutation_DeleteTask,
    } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import Subtasks from "./task-details-subtasks.svelte";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import type { ReadableQuery } from "svelte-apollo";
    import { onDestroy } from "svelte";
    import ToolBar from "./toolBar.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import { getModal } from "../dialogModal.svelte";
    import UserPicker from "../userPicker.svelte";

    let res: ReadableQuery<any> = null;
    let task = null;
    let subTasks = [];
    let taskModified = false;
    let isSaving = false;

    function fieldChanged() {
        taskModified = true;
    }

    let taskWSStrore;

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

            taskWSStrore = getSubscriptionForCollection(
                "task",
                $currenTaskDetailsUUID
            );
        } else {
            reset();
        }
    }

    function setData(data) {
        if (!taskModified) {
            task = { ...data.task };
        }
    }

    let unsubscriber = null;
    $: {
        if (res) {
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
        }
    }

    $: itsNew = $currenTaskDetailsUUID == null;

    $: saveEnabled = taskModified && task.title.length && !isSaving;

    async function save() {
        isSaving = true;
        if (itsNew) {
            try {
                let mRes = await client.mutate({
                    mutation: Mutation_AddTask,
                    variables: {
                        input: {
                            workspaceBoardSectionUuid: $newTaskSectionUUID,
                            ...task,
                        },
                    },
                });

                let taskUUID = mRes.data.addTask.task.uuid;
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
                            title: task.title,
                            description: task.description,
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
        let modalRes = await getModal("deleteTaskConfirmModal").open();

        if (!modalRes) {
            return;
        }

        try {
            let mRes = await client.mutate({
                mutation: Mutation_DeleteTask,
                variables: {
                    input: {
                        uuid: task.uuid,
                    },
                },
                update(cache, { data }) {
                    const sectionUUID = task.workspaceBoardSection.uuid;
                    const cacheId = `WorkspaceBoardSection:${sectionUUID}`;

                    cache.modify({
                        id: cacheId,
                        fields: {
                            tasks(list = []) {
                                return list.filter(
                                    (it) => it.__ref != `Task:${task.uuid}`
                                );
                            },
                        },
                    });
                },
            });

            closeTaskDetails();
        } catch (error) {
            console.error(error);
        }
    }

    let userPickerOpen = false;
    function onUserSelected({ detail: { user } }) {
        console.log(user);
        userPickerOpen = false;
    }
</script>

{#if res && $res.loading}
    <div class="flex flex-col p-0 w-[60vw] justify-center items-center h-full">
        {$_("loading")}
    </div>
{:else}
    <div class="flex flex-col p-0 w-[60vw]">
        <header class="flex p-6 space-x-4 items-center bg-base-100 relative">
            <div
                class="flex justify-center items-center w-11 h-11 rounded-full shrink-0 border-2 border-primary text-primary border-dashed hover:ring"
                on:click={() => (userPickerOpen = !userPickerOpen)}
            >
                <IconPlus />
            </div>
            <input
                class="grow text-xl p-2 rounded-md nowrap-ellipsis"
                placeholder={$_("task-name")}
                on:input={() => fieldChanged()}
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
                class="btn btn-primary rounded-full shrink-0"
                on:click={() => save()}>{$_("save")}</button
            >
            {#if userPickerOpen}
                <div class="absolute top-20 left-2 right-20 max-w-md z-10">
                    <UserPicker
                        workspaceUUID={$currentWorkspaceUUID}
                        selectedUser={task.user}
                        on:userSelected={onUserSelected}
                    />
                </div>
            {/if}
        </header>
        <div class="tabs px-6">
            <button class="tab tab-bordered tab-active">{$_("task")}</button>
            <button class="tab tab-bordered">{$_("discussion")}</button>
            <div class="h-[2px] grow bg-base-300" />
        </div>
        <main class="flex flex-col overflow-y-auto">
            <div class="flex flex-col p-6 space-y-4">
                <div class="text-xl uppercase font-bold">
                    {$_("description")}
                </div>

                <textarea
                    rows="6"
                    class="textarea textarea-bordered resize-none leading-normal p-4"
                    placeholder={$_("please-enter-a-description")}
                    on:input={() => fieldChanged()}
                    bind:value={task.description}
                />
            </div>
            {#if $currenTaskDetailsUUID && subTasks}
                <Subtasks taskUUID={$currenTaskDetailsUUID} {subTasks} />
            {/if}
        </main>
    </div>
{/if}

<style lang="scss">
    main {
        max-height: calc(100vh - 128px);
    }
</style>
