<script lang="ts">
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import IconChevronRight from "../icons/icon-chevron-right.svelte";
    import IconPlus from "../icons/icon-plus.svelte";
    import { openNewTask, openTaskDetails } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";
    import { sortable } from "$lib/actions/sortable";
    import delay from "delay";
    import { client } from "$lib/graphql/client";
    import { Mutation_MoveTask } from "$lib/graphql/operations";

    export let section;
    export let index = 0;

    export let isDragging = false;

    let open = false;
    let firstOpen = open;

    function toggleOpen() {
        open = !open;
        firstOpen = true;
    }

    let contentHeght = 0;
    $: openHeight = open ? contentHeght : 0;
    $: openArrowDeg = open ? 90 : 0;

    function onEdit() {
        console.log("edit");
    }
    function onDelete() {
        console.log("delete");
    }

    function taskDragStart(e) {
        isDragging = true;
    }

    async function taskDragEnd({ detail }) {
        await delay(10);
        isDragging = false;

        let task = section.tasks[detail.oldIndex];
        const fromSectionUUID = detail.from.getAttribute("data-uuid");
        const toSectionUUID = detail.to.getAttribute("data-uuid");
        const order = detail.newIndex;

        if (
            task &&
            (fromSectionUUID != toSectionUUID ||
                detail.newIndex != detail.oldIndex)
        ) {
            moveTask(task.uuid, toSectionUUID, order);
        }
    }

    async function moveTask(taskUuid, workspaceBoardSectionUuid, order) {
        try {
            let mRes = await client.mutate({
                mutation: Mutation_MoveTask,
                variables: {
                    input: {
                        taskUuid,
                        workspaceBoardSectionUuid,
                        order,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }
</script>

<div class="flex m-2 bg-base-100" class:hover:ring={isDragging}>
    <div
        class="w-1 shrink-0"
        style={`background-color: hsl(${index * 36}, 80%, 60%);`}
    />
    <div class="flex grow flex-col">
        <header
            class="drag-handle select-none flex items-center h-16 p-2  children:m-1 cursor-pointer"
            on:click={toggleOpen}
        >
            <div
                class="children:w-5 px-2 transition-transform"
                style="transform: rotate({openArrowDeg}deg);"
            >
                <IconChevronRight />
            </div>
            <div class="grow font-bold uppercase">
                {section.title}
                {#if !open} ({section.tasks.length}) {/if}
            </div>
            {#each [{ label: "Edit", icon: IconEdit, onClick: onEdit }, { label: "Delete", icon: IconTrash, onClick: onDelete }] as it}
                <button
                    class="btn btn-ghost btn-xs h-10 px-3 flex justify-center items-center"
                    on:click|stopPropagation={it.onClick}
                >
                    <svelte:component this={it.icon} />
                    <span>{it.label}</span>
                </button>
            {/each}
        </header>
        <main style="--open-height:{openHeight}px">
            {#if firstOpen}
                <div
                    class="content p-2 flex flex-wrap"
                    bind:clientHeight={contentHeght}
                    use:sortable={{ group: "Tasks" }}
                    on:dragStart={taskDragStart}
                    on:dragEnd={taskDragEnd}
                    data-uuid={section.uuid}
                >
                    {#each section.tasks as task, inx (task.uuid)}
                        <div
                            class="item h-24 bg-base-100 m-2 rounded-lg p-4 flex items-center border border-base-300 overflow-y-hidden cursor-pointer"
                            class:hover:ring={!isDragging}
                            on:click={() =>
                                !isDragging && openTaskDetails(task.uuid)}
                        >
                            <div
                                class="m-2 mr-3 flex overflow-hidden w-11 h-11 rounded-full shrink-0 border-2 border-primary "
                            >
                                <img
                                    width="100%"
                                    height="100%"
                                    src="https://picsum.photos/seed/picsum/200?random={inx}"
                                    alt="user"
                                />
                            </div>
                            <div
                                class="flex flex-col overflow-y-hidden max-h-full mr-3"
                            >
                                <div class="flex items-center">
                                    <div
                                        class="text-xs bg-secondary px-2 py-1 rounded mr-2 font-bold"
                                    >
                                        Design
                                    </div>
                                    <div class="text-xs">Date 2022.01.01</div>
                                </div>
                                <div
                                    class="flex flex-col px-1 max-w-xs overflow-y-hidden overflow-ellipsis font-bold"
                                >
                                    {task.title}
                                </div>
                            </div>
                        </div>
                    {/each}
                    {#if !isDragging}
                        <div
                            class="ignore-elements h-24 bg-base-100 m-2 rounded-lg p-4 flex items-center border border-base-300 overflow-y-hidden cursor-pointer hover:ring"
                            on:click={() => openNewTask(section.uuid)}
                        >
                            <div
                                class="m-2 mr-3 flex justify-center items-center overflow-hidden w-11 h-11 rounded-full shrink-0 border-2 border-primary text-primary border-dashed"
                            >
                                <IconPlus />
                            </div>
                            <div
                                class="flex flex-col overflow-y-hidden max-h-full mr-3 text-primary font-bold"
                            >
                                {$_("new-task")}
                            </div>
                        </div>
                    {/if}
                </div>
            {/if}
        </main>
    </div>
</div>

<style lang="scss">
    main {
        --open-height: 0;
        overflow: hidden;
        position: relative;
        height: var(--open-height);
        transition: height 300ms ease-in-out;
    }

    main > .content {
        transition: transform 300ms ease-in-out;
        position: absolute;
    }

    :global(.sortable-ghost) {
        opacity: 0;
    }
</style>
