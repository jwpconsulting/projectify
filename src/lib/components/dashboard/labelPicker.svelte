<script lang="ts">
    import { client } from "$lib/graphql/client";
    import { Mutation_AssignLabel } from "$lib/graphql/operations";

    import { createEventDispatcher, onMount } from "svelte";

    import ColorDot from "../colorDot.svelte";
    import LabelList from "./labelList.svelte";
    import TaskDetails from "./task-details.svelte";

    let searchText = "";
    export let task;
    export let selectedLabels = [];
    let rootEl;

    let dispatch = createEventDispatcher();

    onMount(() => {
        rootEl.focus();
    });

    function onBlur(event) {
        if (!event.currentTarget.contains(event.relatedTarget)) {
            dispatch("blur");
        }
    }

    async function assignLabel(label, assigned) {
        try {
            await client.mutate({
                mutation: Mutation_AssignLabel,
                variables: {
                    input: {
                        taskUuid: task.uuid,
                        labelUuid: label.uuid,
                        assigned,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }
</script>

<div
    tabindex="-1"
    class="flex flex-col overflow-hidden w-full bg-base-100 shadow-lg rounded-xl divide-y divide-base-300 max-h-[400px]"
    bind:this={rootEl}
    on:blur={onBlur}
>
    <div class="p-4 font-bold">Apply labels to this task</div>
    <div class="p-4">
        <input
            type="text"
            class="input w-full input-bordered"
            placeholder="Filter labels"
            bind:value={searchText}
            on:blur={() => rootEl.focus()}
        />
    </div>
    <div
        class="flex flex-col divide-y divide-base-300 overflow-y-auto max-h-full"
    >
        <LabelList
            bind:searchText
            bind:selectedLabels
            editable={true}
            let:label
            let:active
            on:addLabel={({ detail }) => {
                assignLabel(detail, true);
            }}
            on:removeLabel={({ detail }) => {
                assignLabel(detail, false);
            }}
        >
            <div
                slot="item"
                class="px-4 flex items-center space-x-2 h-14  hover:bg-base-200 select-none"
            >
                <div class="w-6 h-6 bg-debug rounded-full shrink-0">
                    <ColorDot index={label.color} {active} />
                </div>
                <div class="grid">
                    <span class="nowrap-ellipsis">{label.name}</span>
                </div>
            </div>
        </LabelList>
    </div>
</div>
