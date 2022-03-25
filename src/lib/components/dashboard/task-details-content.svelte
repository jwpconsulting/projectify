<script lang="ts">
    import { currenTaskDetailsUUID } from "$lib/stores/dashboard";

    import { _ } from "svelte-i18n";
    import LabelPicker from "./labelPicker.svelte";
    import LabelList from "./labelList.svelte";

    import Subtasks from "./task-details-subtasks.svelte";
    import ToolBar from "./toolBar.svelte";
    import IconEdit from "../icons/icon-edit.svelte";

    export let task;
    export let subTasks;
    export let labels;
    export let taskModified = false;

    let labelPickerOpen = false;
</script>

{#if task}
    <main class="flex flex-col space-y-6 py-4 px-6">
        <div class="flex flex-col space-y-4">
            <div class="text-xl uppercase font-bold">
                {$_("description")}
            </div>
            <textarea
                rows="6"
                class="textarea textarea-bordered resize-none leading-normal p-4"
                placeholder={$_("please-enter-a-description")}
                on:input={() => (taskModified = true)}
                bind:value={task.description}
            />
            <div class="relative">
                <div class="flex items-center border-b border-base-300 py-2">
                    <div class="text-xl uppercase font-bold grow">
                        {"Labels"}
                    </div>

                    <div>
                        <ToolBar
                            items={[
                                {
                                    label: $_("Edit"),
                                    icon: IconEdit,
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
                        class="absolute top-0 left-0 right-20 max-w-md z-10 pb-6"
                    >
                        <LabelPicker
                            {task}
                            bind:selectedLabels={labels}
                            on:blur={() => (labelPickerOpen = false)}
                        />
                    </div>
                {/if}
            </div>
            <div class="inline-flex gap-2 flex-wrap">
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
