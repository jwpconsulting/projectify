<script>
    import {
        currenTaskDetailsUUID,
        newTaskSectionUUID,
        closeTaskDetails,
    } from "$lib/stores/dashboard";
    import IconPlus from "../icons/icon-plus.svelte";

    import {
        Query_DashboardTaskDetais,
        Mutation_AddTask,
    } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import IconTrash from "../icons/icon-trash.svelte";
    import { client } from "$lib/graphql/client";

    let res = null;
    let task = null;
    let percent = 0;
    let subTasks = [];
    let firstLoad = false;
    let newSubTaskTitle = null;

    let itsNew = $currenTaskDetailsUUID == null;

    function reset() {
        res = null;
        task = {
            title: "",
            description: "",
        };
        percent = 0;
        subTasks = [];
    }

    $: {
        if ($currenTaskDetailsUUID) {
            res = query(Query_DashboardTaskDetais, {
                variables: { uuid: $currenTaskDetailsUUID },
            });
            firstLoad = true;
        } else {
            reset();
        }
    }

    $: {
        if (res && $res.data && firstLoad) {
            firstLoad = false;
            task = $res.data.task;
            subTasks = task.subTasks.map((t) => {
                return {
                    ...t,
                    checked: Boolean(t.checked),
                };
            });
        }
    }

    $: {
        if (subTasks.length) {
            let sum = 0;
            subTasks.forEach((it) => {
                sum += it.checked;
            });
            percent = Math.round((sum / subTasks.length) * 100);
        }
    }

    function addSubTask() {
        if (!newSubTaskTitle || newSubTaskTitle.length < 1) {
            return;
        }
        subTasks = [
            ...subTasks,
            {
                title: newSubTaskTitle,
                checked: false,
            },
        ];
        newSubTaskTitle = "";
    }

    function removeSubTask(inx) {
        subTasks.splice(inx, 1);
        subTasks = subTasks;
    }

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
                reset();
                closeTaskDetails();
            } catch (error) {
                console.error(error);
            }
        }
    }
</script>

{#if res && $res.loading}
    <div class="flex flex-col p-0 w-[60vw] justify-center items-center h-full">
        Loading...
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
                placeholder="Task Name"
                bind:value={task.title}
            />

            <button
                class="btn btn-primary rounded-full"
                on:click={() => save()}>Save</button
            >
        </header>
        <div class="tabs px-6">
            <button class="tab tab-bordered tab-active">Task</button>
            <button class="tab tab-bordered">Discussion</button>
            <div class="h-[2px] grow bg-base-300" />
        </div>
        <main class="flex flex-col overflow-y-auto">
            <div class="flex flex-col p-6 space-y-4">
                <div class="text-xl uppercase font-bold">Overview</div>

                <textarea
                    rows="6"
                    class="textarea textarea-bordered resize-none leading-normal p-4"
                    placeholder="Please enter an overview"
                    bind:value={task.description}
                />
            </div>
            <div class="flex flex-col p-6 space-y-4">
                <div class="flex text-xl space-x-2">
                    <span class="uppercase font-bold">Sub Task</span>
                    <span>{percent}%</span>
                </div>

                <progress
                    class="progress progress-primary"
                    value={percent}
                    max="100"
                />

                <div>
                    {#each subTasks as it, inx}
                        <label class="cursor-pointer label space-x-2">
                            <input
                                type="checkbox"
                                class="checkbox checkbox-primary"
                                bind:checked={it.checked}
                            />
                            <div class="grow">{it.title}</div>
                            <button
                                on:click={() => removeSubTask(inx)}
                                class="btn btn-xs btn-circle btn-ghost children:w-2"
                                ><IconTrash /></button
                            >
                        </label>
                    {/each}
                </div>

                <div class="relative">
                    <input
                        type="text"
                        placeholder="New sub task name"
                        class="w-full pr-16 input input-bordered"
                        bind:value={newSubTaskTitle}
                        on:keydown={(e) => e.key === "Enter" && addSubTask()}
                    />
                    <button
                        on:click={() => addSubTask()}
                        class="absolute top-0 right-0 rounded-l-none btn btn-primary btn-square"
                        ><IconPlus /></button
                    >
                </div>
            </div>
        </main>
    </div>
{/if}

<style lang="scss">
    main {
        max-height: calc(100vh - 128px);
    }

    ::-webkit-progress-value {
        transition: width 1s;
    }
</style>
