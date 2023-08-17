<script lang="ts">
    import lodash from "lodash";
    import { tick } from "svelte";
    import { _ } from "svelte-i18n";

    import IconChevronDown from "$lib/components/icons/icon-chevron-down.svelte";
    import IconChevronUp from "$lib/components/icons/icon-chevron-up.svelte";
    import IconClose from "$lib/components/icons/icon-close.svelte";
    import IconEdit from "$lib/components/icons/icon-edit.svelte";
    import IconPlus from "$lib/components/icons/icon-plus.svelte";
    import IconTrash from "$lib/components/icons/icon-trash.svelte";
    import IconUpload from "$lib/components/icons/icon-upload.svelte";
    import { client } from "$lib/graphql/client";
    import {
        Mutation_AddSubTask,
        Mutation_ChangeSubTaskDone,
        Mutation_DeleteSubTaskMutation,
        Mutation_MoveSubTaskMutation,
        Mutation_UpdateSubTask,
    } from "$lib/graphql/operations";
    import type { SubTask } from "$lib/types/workspace";

    export let taskUuid: string;
    export let subTasks: SubTask[];
    let percent = 0;
    let newSubTaskTitle = "";

    $: {
        if (subTasks.length) {
            const sum = lodash.sumBy(subTasks, (it) => (it.done ? 1 : 0));
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
                uuid: "",
                done: false,
                created: "",
                modified: "",
                order: 0,
            },
        ];

        if (taskUuid) {
            try {
                await client.mutate({
                    mutation: Mutation_AddSubTask,
                    variables: {
                        input: {
                            taskUuid: taskUuid,
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

    async function changeSubTaskDone(subTask: SubTask) {
        if (!subTask || !subTask.uuid) {
            return;
        }

        try {
            await client.mutate({
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

    async function deleteSubTask(subTask: SubTask) {
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
            await client.mutate({
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

    async function moveSubTask(subTask: SubTask, order: number) {
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

    async function moveUp(subTask: SubTask) {
        await moveSubTask(subTask, subTask.order - 1);
    }
    async function moveDown(subTask: SubTask) {
        await moveSubTask(subTask, subTask.order + 1);
    }

    let subtaskEditTitle: string | null = null;
    let editSubtaskUuid: string | null = null;
    let editSubtaskInput: HTMLElement | null = null;

    async function editSubtask(subTask: SubTask) {
        editSubtaskUuid = subTask.uuid;
        subtaskEditTitle = subTask.title;

        await tick();

        if (!editSubtaskInput) {
            throw new Error("Expected editSubtaskInput");
        }
        editSubtaskInput.focus();
    }
    function stopEditSubtask() {
        editSubtaskUuid = null;
        subtaskEditTitle = null;
    }

    async function saveSubTask(subTask: SubTask) {
        if (!subtaskEditTitle) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_UpdateSubTask,
                variables: {
                    input: {
                        uuid: subTask.uuid,
                        title: subtaskEditTitle,
                        description: "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }

        subTask.title = subtaskEditTitle;
        editSubtaskUuid = null;
    }
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
                    on:change={(_e) => changeSubTaskDone(it)}
                />

                {#if editSubtaskUuid == it.uuid}
                    <div class="relative flex w-full grow">
                        <input
                            bind:this={editSubtaskInput}
                            class="nowrap-ellipsis input input-sm grow rounded-md p-2 text-base"
                            on:keydown={(e) => {
                                if (e.key === "Enter") {
                                    saveSubTask(it);
                                } else if (e.key == "Escape") {
                                    stopEditSubtask();
                                }
                            }}
                            bind:value={subtaskEditTitle}
                        />
                        <button
                            class="btn btn-ghost btn-square btn-sm absolute right-0 h-full w-8 rounded-l-none"
                            on:click={() => stopEditSubtask()}
                        >
                            <IconClose />
                        </button>
                    </div>
                {:else}
                    <div class="grow">{it.title}</div>
                {/if}

                {#if it.uuid}
                    <div class="flex gap-2">
                        <button
                            disabled={inx == 0}
                            on:click={() => moveUp(it)}
                            class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                            ><IconChevronUp /></button
                        >
                        <button
                            disabled={subTasks.length == inx + 1}
                            on:click={() => moveDown(it)}
                            class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                            ><IconChevronDown /></button
                        >

                        {#if editSubtaskUuid == it.uuid}
                            <button
                                on:click={() => saveSubTask(it)}
                                class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                                ><IconUpload /></button
                            >
                        {:else}
                            <button
                                on:click={() => editSubtask(it)}
                                class="btn btn-ghost btn-xs h-9 w-9 rounded-full"
                                ><IconEdit /></button
                            >
                        {/if}

                        <button
                            on:click={() => deleteSubTask(it)}
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
            class="btn btn-primary btn-square absolute right-0 top-0 rounded-l-none"
            ><IconPlus /></button
        >
    </div>
</div>
