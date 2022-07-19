<script lang="ts">
    import { currentTaskDetailsUuid } from "$lib/stores/dashboard";

    import { _ } from "svelte-i18n";
    import LabelPicker from "./labelPicker.svelte";
    import LabelList from "./labelList.svelte";

    import Subtasks from "./task-details-subtasks.svelte";
    import ToolBar from "./toolBar.svelte";
    import InputDatePicker from "../inputDatePicker.svelte";
    import IconCheckCircle from "../icons/icon-check-circle.svelte";
    import RichTextarea from "../rich-textarea.svelte";
    import type { Task, SubTask, Label } from "$lib/types";

    export let task: Task;
    export let subTasks: SubTask[];
    export let labels: Label[];
    export let taskModified = false;

    let labelPickerOpen = false;
</script>

{#if task}
    <main class="flex flex-col gap-4 py-6 px-4">
        <div class="flex flex-col gap-8 pt-4">
            <div class="flex flex-col gap-4">
                <div class="text-xl font-bold uppercase">
                    {$_("description")}
                </div>
                <RichTextarea
                    bind:content={task.description}
                    placeholder={$_("please-enter-a-description")}
                    bind:modified={taskModified}
                />
            </div>

            <div class="flex flex-col gap-4">
                <div class="text-xl font-bold uppercase">
                    {$_("deadline")}
                </div>
                <div>
                    <InputDatePicker
                        input={{
                            value: task.deadline,
                        }}
                        placeholder={$_("deadline")}
                        on:change={({ detail: { date } }) => {
                            task.deadline = date;
                            taskModified = true;
                        }}
                    />
                </div>
            </div>

            <div class="flex flex-col gap-6 pb-4">
                <div class="relative">
                    <div
                        class="flex items-center border-b border-base-300 py-2"
                    >
                        <div class="grow text-xl font-bold uppercase">
                            {"Labels"}
                        </div>

                        <div>
                            <ToolBar
                                items={[
                                    {
                                        label: $_("apply-labels"),
                                        icon: IconCheckCircle,
                                        onClick: () => {
                                            labelPickerOpen = true;
                                        },
                                    },
                                ]}
                            />
                        </div>
                    </div>
                    {#if labelPickerOpen}
                        <div
                            class="absolute top-0 left-0 right-20 z-10 max-w-md pb-6"
                        >
                            <LabelPicker
                                {task}
                                bind:selectedLabels={labels}
                                on:blur={() => (labelPickerOpen = false)}
                            />
                        </div>
                    {/if}
                </div>
                <div class="inline-flex flex-wrap gap-2">
                    <LabelList
                        bind:labels
                        editable={false}
                        on:addLabelClick={() => (labelPickerOpen = true)}
                    />
                </div>
            </div>
        </div>
        {#if subTasks && $currentTaskDetailsUuid}
            <Subtasks taskUuid={$currentTaskDetailsUuid} bind:subTasks />
        {/if}
    </main>
{/if}
