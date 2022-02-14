<script lang="ts">
    import {
        currenTaskDetailsUUID,
        newTaskSectionUUID,
        closeTaskDetails,
    } from "$lib/stores/dashboard";
    import IconPlus from "../icons/icon-plus.svelte";

    import {
        Query_DashboardTaskDetails,
        Mutation_AddTask,
    } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import Subtasks from "./task-details-subtasks.svelte";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import type { ReadableQuery } from "svelte-apollo";

    let res: ReadableQuery<any> = null;
    let task = null;
    let subTasks = [];

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
    }, 1000);

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

    $: {
        if ($taskWSStrore) {
            refetch();
        }
    }

    $: {
        if (res && $res.data) {
            task = $res.data.task;
            subTasks = task.subTasks.map((t) => {
                return {
                    ...t,
                    done: Boolean(t.done),
                };
            });
        }
    }

    $: itsNew = $currenTaskDetailsUUID == null;

    $: saveEnabled =
        task && task.title.length > 0 && task.description.length > 0;

    async function save() {
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
                currenTaskDetailsUUID.set(mRes.data.addTask.task.uuid);
            } catch (error) {
                console.error(error);
            }
        } else {
            reset();
            closeTaskDetails();
        }
    }
</script>

{#if res && $res.loading}
    <div class="flex flex-col p-0 w-[60vw] justify-center items-center h-full">
        {$_("loading")}
    </div>
{:else}
    <div class="flex flex-col p-0 w-[60vw]">
        <header class="flex p-6 space-x-4 items-center bg-base-100">
            <div
                class="flex justify-center items-center overflow-hidden w-11 h-11 rounded-full shrink-0 border-2 border-primary text-primary border-dashed hover:ring"
            >
                <IconPlus />
            </div>
            <input
                class="grow text-xl p-2 rounded-md"
                placeholder={$_("task-name")}
                bind:value={task.title}
            />

            <button
                disabled={!saveEnabled}
                class="btn btn-primary rounded-full"
                on:click={() => save()}>{$_("save")}</button
            >
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
