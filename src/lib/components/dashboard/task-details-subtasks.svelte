<script lang="ts">
    import {
        Mutation_AddSubTask,
        Mutation_ChangeSubTaskDone,
        Mutation_DeleteSubTaskMutation,
        Mutation_MoveSubTaskMutation,
    } from "$lib/graphql/operations";

    import { client } from "$lib/graphql/client";
    import IconTrash from "../icons/icon-trash.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import { _ } from "svelte-i18n";
    import IconChevronDown from "../icons/icon-chevron-down.svelte";
    import IconChevronUp from "../icons/icon-chevron-up.svelte";
    import IconEdit from "../icons/icon-edit.svelte";

    export let taskUUID;
    export let subTasks;
    let percent = 0;
    let newSubTaskTitle = "";

    $: {
        if (subTasks.length) {
            let sum = 0;
            subTasks.forEach((it) => {
                sum += it.done;
            });
            percent = Math.round((sum / subTasks.length) * 100);
        }
    }

    async function addSubTask() {
        if (!newSubTaskTitle || newSubTaskTitle.length < 1) {
            return;
        }
        subTasks = [
            ...subTasks,
            {
                title: newSubTaskTitle,
                done: false,
            },
        ];

        if (taskUUID) {
            try {
                let mRes = await client.mutate({
                    mutation: Mutation_AddSubTask,
                    variables: {
                        input: {
                            taskUuid: taskUUID,
                            title: newSubTaskTitle,
                            description: "",
                        },
                    },
                });
            } catch (error) {
                console.error(error);
            }
        }

        newSubTaskTitle = "";
    }

    async function changeSubTaskDone(subTask) {
        if (!subTask || !subTask.uuid) {
            return;
        }

        try {
            let mRes = await client.mutate({
                mutation: Mutation_ChangeSubTaskDone,
                variables: {
                    input: {
                        subTaskUuid: subTask.uuid,
                        done: subTask.done,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function deleteSubTask(subTask) {
        if (!subTask || !subTask.uuid) {
            return;
        }

        const inx = subTasks.findIndex((it) => subTask.uuid == it.uuid);
        if (inx == -1) {
            return;
        }
        subTasks.splice(inx, 1);
        subTasks = subTasks;

        try {
            let mRes = await client.mutate({
                mutation: Mutation_DeleteSubTaskMutation,
                variables: {
                    input: {
                        uuid: subTask.uuid,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function moveSubTask(subTask, order) {
        try {
            await client.mutate({
                mutation: Mutation_MoveSubTaskMutation,
                variables: {
                    input: {
                        subTaskUuid: subTask.uuid,
                        order,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function moveUp(subTask) {
        await moveSubTask(subTask, subTask.order - 1);
    }
    async function moveDown(subTask) {
        await moveSubTask(subTask, subTask.order + 1);
    }

    async function edit(subTask) {}
</script>

<div class="flex flex-col space-y-4">
    <div class="flex space-x-2 text-xl">
        <span class="font-bold uppercase">{$_("sub-task")}</span>
        <span>{percent}%</span>
    </div>

    <progress
        class="progress progress-primary w-full grow bg-base-300"
        value={percent}
        max="100"
    />

    <div>
        {#each subTasks as it, inx}
            <label
                class="label flex cursor-pointer items-center justify-start gap-4 rounded-lg p-2 hover:bg-base-200"
            >
                <input
                    type="checkbox"
                    class="checkbox checkbox-primary shrink-0"
                    bind:checked={it.done}
                    on:change={(e) => changeSubTaskDone(it)}
                />
                <div class="grow">{it.title}</div>
                {#if it.uuid}
                    <div class="flex gap-2">
                        <button
                            disabled={inx == 0}
                            on:click={() => moveUp(it)}
                            class:visible={it.uuid}
                            class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                            ><IconChevronUp /></button
                        >
                        <button
                            disabled={subTasks.length == inx + 1}
                            on:click={() => moveDown(it)}
                            class:visible={it.uuid}
                            class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                            ><IconChevronDown /></button
                        >
                        <button
                            on:click={() => edit(it)}
                            class:visible={it.uuid}
                            class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                            ><IconEdit /></button
                        >
                        <button
                            on:click={() => deleteSubTask(it)}
                            class:visible={it.uuid}
                            class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                            ><IconTrash /></button
                        >
                    </div>
                {/if}
            </label>
        {/each}
    </div>

    <div class="relative">
        <input
            type="text"
            placeholder={$_("new-sub-task-name")}
            class="input input-bordered w-full pr-16"
            bind:value={newSubTaskTitle}
            on:keydown={(e) => e.key === "Enter" && addSubTask()}
        />
        <button
            disabled={newSubTaskTitle.length < 1}
            on:click={() => addSubTask()}
            class="btn btn-primary btn-square absolute top-0 right-0 rounded-l-none"
            ><IconPlus /></button
        >
    </div>
</div>
