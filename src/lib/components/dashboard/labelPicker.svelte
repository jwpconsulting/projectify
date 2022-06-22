<script lang="ts">
    import { client } from "$lib/graphql/client";
    import { Mutation_AssignLabel } from "$lib/graphql/operations";
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";

    import { createEventDispatcher, onMount } from "svelte";

    import ColorDot from "../colorDot.svelte";
    import LabelList from "./labelList.svelte";

    let searchText = "";
    export let task;
    export let selectedLabels = [];
    let rootEl;

    export let dispatch = createEventDispatcher();

    onMount(() => {
        rootEl.focus();
    });

    function onBlur(event) {
        if (!event.currentTarget.contains(event.relatedTarget)) {
            dispatch("blur");
        }
    }

    async function assignLabel(label, assigned) {
        if (!task?.uuid) {
            return;
        }

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

    let serachFieldEl;
    $: {
        if (serachFieldEl) {
            serachFieldEl.focus();
        }
    }
</script>

<div
    tabindex="-1"
    class="flex max-h-[400px] w-full flex-col divide-y divide-base-300 overflow-hidden rounded-xl bg-base-100 shadow-lg"
    bind:this={rootEl}
    on:blur={onBlur}
>
    <div class="p-4 font-bold">Apply labels to this task</div>
    <div class="p-4">
        <input
            type="text"
            class="input input-bordered w-full"
            placeholder="Filter labels"
            bind:value={searchText}
            bind:this={serachFieldEl}
            on:blur={() => rootEl.focus()}
        />
    </div>
    <div
        class="flex max-h-full flex-col divide-y divide-base-300 overflow-y-auto"
    >
        <LabelList
            labels={$currentWorkspaceLabels}
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
                class="flex h-14 select-none items-center space-x-2  px-4 hover:bg-base-200"
            >
                <div class="bg-debug h-6 w-6 shrink-0 rounded-full">
                    <ColorDot index={label.color} {active} />
                </div>
                <div class="grid">
                    <span class="nowrap-ellipsis">{label.name}</span>
                </div>
            </div>
        </LabelList>
    </div>
</div>
