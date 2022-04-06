<script lang="ts">
    import { currenTaskDetailsUUID } from "$lib/stores/dashboard";

    import { _ } from "svelte-i18n";
    import LabelPicker from "./labelPicker.svelte";
    import LabelList from "./labelList.svelte";

    import Subtasks from "./task-details-subtasks.svelte";
    import ToolBar from "./toolBar.svelte";
    import InputDatePicker from "../inputDatePicker.svelte";
    import IconCheckCircle from "../icons/icon-check-circle.svelte";

    export let task;
    export let subTasks;
    export let labels;
    export let taskModified = false;

    let labelPickerOpen = false;
</script>

{#if task}
    <main class="flex flex-col space-y-6 py-4 px-6">
        <div class="flex flex-col space-y-4">
            <div class="text-xl font-bold uppercase">
                {$_("description")}
            </div>
            <textarea
                rows="6"
                class="textarea textarea-bordered resize-none p-4 leading-normal"
                placeholder={$_("please-enter-a-description")}
                on:input={() => (taskModified = true)}
                bind:value={task.description}
            />
            <div>
                <InputDatePicker
                    input={{
                        value: task.deadline,
                    }}
                    placeholder={"Deadline"}
                />
            </div>
            <div class="relative">
                <div class="flex items-center border-b border-base-300 py-2">
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
                    {labels}
                    editable={false}
                    on:addLabelClick={() => (labelPickerOpen = true)}
                />
            </div>
        </div>
        {#if $currenTaskDetailsUUID && subTasks}
            <Subtasks taskUUID={$currenTaskDetailsUUID} {subTasks} />
        {/if}
    </main>
{/if}
