<script lang="ts">
    import {
        Mutation_AddSubTask,
        Mutation_ChangeSubTaskDone,
        Mutation_DeleteSubTaskMutation,
    } from "$lib/graphql/operations";

    import { client } from "$lib/graphql/client";
    import IconTrash from "../icons/icon-trash.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import { _ } from "svelte-i18n";

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
</script>

<div class="flex flex-col p-6 space-y-4">
    <div class="flex text-xl space-x-2">
        <span class="uppercase font-bold">{$_("sub-task")}</span>
        <span>{percent}%</span>
    </div>

    <progress class="progress progress-primary" value={percent} max="100" />

    <div>
        {#each subTasks as it, inx}
            <label class="cursor-pointer label space-x-2 hover:bg-base-200">
                <input
                    type="checkbox"
                    class="checkbox checkbox-primary"
                    bind:checked={it.done}
                    on:change={(e) => changeSubTaskDone(it)}
                />
                <div class="grow">{it.title}</div>
                <button
                    on:click={() => deleteSubTask(it)}
                    class="btn btn-xs btn-circle btn-ghost children:w-2"
                    ><IconTrash /></button
                >
            </label>
        {/each}
    </div>

    <div class="relative">
        <input
            type="text"
            placeholder={$_("new-sub-task-name")}
            class="w-full pr-16 input input-bordered"
            bind:value={newSubTaskTitle}
            on:keydown={(e) => e.key === "Enter" && addSubTask()}
        />
        <button
            disabled={newSubTaskTitle.length < 1}
            on:click={() => addSubTask()}
            class="absolute top-0 right-0 rounded-l-none btn btn-primary btn-square"
            ><IconPlus /></button
        >
    </div>
</div>
