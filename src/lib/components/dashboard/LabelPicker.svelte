<script lang="ts">
    import { client } from "$lib/graphql/client";
    import { Mutation_AssignLabel } from "$lib/graphql/operations";
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import type { Task, Label } from "$lib/types/workspace";
    import LabelPill from "$lib/components/dashboard/LabelPill.svelte";

    import { createEventDispatcher, onMount } from "svelte";

    import LabelList from "./LabelList.svelte";

    let searchText = "";
    export let task: Task;
    export let selectedLabels: Label[] = [];
    let rootEl: HTMLElement;

    export let dispatch = createEventDispatcher();

    onMount(() => {
        rootEl.focus();
    });

    function onBlur(event: FocusEvent) {
        const currentTarget = event.currentTarget;
        const relatedTarget = event.relatedTarget;
        if (
            currentTarget instanceof HTMLElement &&
            relatedTarget instanceof HTMLElement
        ) {
            if (!currentTarget.contains(relatedTarget)) {
                dispatch("blur");
            }
        } else {
            throw new Error("Invalid currentTarget");
        }
    }

    async function assignLabel(label: Label, assigned: boolean) {
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

    let searchFieldEl: HTMLElement;
    $: {
        if (searchFieldEl) {
            searchFieldEl.focus();
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
            bind:this={searchFieldEl}
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
                <LabelPill {label} />
            </div>
        </LabelList>
    </div>
</div>
