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
    import {
        Mutation_DeleteWorkspaceBoardSection,
        Mutation_MoveTask,
        Mutation_UpdateWorkspaceBoardSection,
    } from "$lib/graphql/operations";
    import ToolBar from "./toolBar.svelte";
    import { getModal } from "../dialogModal.svelte";
    import { dashboardSectionsLayout } from "$lib/stores/dashboard-ui";
    import BoardTaskItem from "./board-task-item.svelte";

    export let boardUUID;
    export let section;
    export let index = 0;

    export let isDragging = false;

    let open = true;
    let firstOpen = open;

    function toggleOpen() {
        if (isDragging) {
            return;
        }
        open = !open;
        firstOpen = true;
    }

    let contentHeght = 0;
    $: openHeight = open ? contentHeght : 0;
    $: openArrowDeg = open ? 90 : 0;

    async function onEdit() {
        let modalRes = await getModal("editBoardSectionModal").open(section);

        if (!modalRes) {
            return;
        }

        try {
            let mRes = await client.mutate({
                mutation: Mutation_UpdateWorkspaceBoardSection,
                variables: {
                    input: {
                        uuid: section.uuid,
                        title: modalRes.outputs.title,
                        description: "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onDelete() {
        let modalRes = await getModal("deleteBoardSectionConfirmModal").open();

        if (!modalRes) {
            return;
        }

        try {
            let mRes = await client.mutate({
                mutation: Mutation_DeleteWorkspaceBoardSection,
                variables: {
                    input: {
                        uuid: section.uuid,
                    },
                },
                update(cache, { data }) {
                    cache.modify({
                        id: `WorkspaceBoard:${boardUUID}`,
                        fields: {
                            sections(currentSections = []) {
                                return currentSections.filter(
                                    (it) =>
                                        it.__ref !=
                                        `WorkspaceBoardSection:${section.uuid}`
                                );
                            },
                        },
                    });
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    function taskDragStart() {
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

    function onHandlerOver(e) {
        if (isDragging) {
            open = true;
            firstOpen = true;
        }
    }

    $: layoutClass = `layout-${$dashboardSectionsLayout}`;
</script>

<div
    class={`${layoutClass} section m-2 flex select-none bg-base-100 shadow-sm`}
>
    <div class="flex grow flex-col">
        <header
            class:open
            class="drag-handle relative flex h-16 cursor-pointer select-none  items-center p-2"
            on:click={$dashboardSectionsLayout == "columns"
                ? null
                : toggleOpen}
            on:focus={onHandlerOver}
            on:mouseover={onHandlerOver}
        >
            {#if $dashboardSectionsLayout != "columns"}
                <div
                    class="px-2 transition-transform"
                    style="transform: rotate({openArrowDeg}deg);"
                >
                    <IconChevronRight />
                </div>
            {/if}
            <div class="ml-2 grid grow font-bold uppercase">
                <span class="nowrap-ellipsis">
                    {section.title}
                    {#if !open} ({section.tasks.length}) {/if}
                </span>
            </div>
            <ToolBar
                items={[
                    { label: $_("Edit"), icon: IconEdit, onClick: onEdit },
                    {
                        label: $_("Delete"),
                        icon: IconTrash,
                        onClick: onDelete,
                        disabled:
                            section.totalTasksCount || section.tasks.length,
                        tooltip: section.tasks.length
                            ? $_("remove-section-tooltip-message")
                            : "",
                    },
                ]}
            />
        </header>
        <main
            style="--open-height:{openHeight}px"
            class:hover:ring={isDragging}
        >
            {#if firstOpen}
                <div
                    class="content min-h-16 relative w-full grow p-2"
                    bind:clientHeight={contentHeght}
                    use:sortable={{ group: "Tasks" }}
                    on:dragStart={taskDragStart}
                    on:dragEnd={taskDragEnd}
                    data-uuid={section.uuid}
                >
                    {#each section.tasks as task (task.uuid)}
                        <BoardTaskItem
                            layout={$dashboardSectionsLayout}
                            {task}
                            showHoverRing={!isDragging}
                            on:click={() =>
                                !isDragging && openTaskDetails(task.uuid)}
                        />
                    {/each}
                    {#if !isDragging}
                        <BoardTaskItem
                            layout={$dashboardSectionsLayout}
                            on:click={() => openNewTask(section.uuid)}
                        />
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

    header {
        &::after {
            content: "";
            position: absolute;

            height: 1px;
            @apply bottom-0 left-3 right-3 bg-base-300;
            transition: all 300ms ease-in-out;
            opacity: 0;
        }

        &.open {
            &::after {
                opacity: 1;
            }
        }
    }

    .section {
        &.layout-grid {
            .content {
                @apply grid;
                grid-auto-flow: row dense;
                grid-template-columns: repeat(auto-fit, minmax(480px, 1fr));
            }
        }
        &.layout-list {
            .content {
                @apply flex flex-col;
            }
        }
        &.layout-columns {
            max-height: calc(100% - 16px);
            main {
                @apply overflow-y-auto;
            }
            .content {
                @apply flex flex-col;
            }
        }
    }
</style>
