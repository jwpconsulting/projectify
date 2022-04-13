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
    import UserProfilePicture from "../userProfilePicture.svelte";
    import { getColorFromInx } from "$lib/utils/colors";
    import { dateStringToLocal } from "$lib/utils/date";
    import { dashboardSectionsLayout } from "$lib/stores/dashboard-ui";

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
</script>

<div class="section m-2 flex select-none bg-base-100">
    <div
        class="w-1 shrink-0"
        style={`background-color: hsl(${index * 45}, 80%, 75%);`}
    />
    <div class="flex grow flex-col">
        <header
            class="drag-handle children:m-1 flex h-16 cursor-pointer select-none  items-center p-2"
            on:click={toggleOpen}
            on:focus={onHandlerOver}
            on:mouseover={onHandlerOver}
        >
            <div
                class="children:w-5 px-2 transition-transform"
                style="transform: rotate({openArrowDeg}deg);"
            >
                <IconChevronRight />
            </div>
            <div class="grid grow font-bold uppercase">
                <span class="nowrap-ellipsis"
                    >{section.order} -
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
                    class:layout-grid={$dashboardSectionsLayout == "grid"}
                    class:layout-list={$dashboardSectionsLayout == "list"}
                    class="content min-h-16 relative w-full grow p-2"
                    bind:clientHeight={contentHeght}
                    use:sortable={{ group: "Tasks" }}
                    on:dragStart={taskDragStart}
                    on:dragEnd={taskDragEnd}
                    data-uuid={section.uuid}
                >
                    {#each section.tasks as task (task.uuid)}
                        <div
                            class="drag-handle item"
                            class:hover:ring={!isDragging}
                            on:click={() =>
                                !isDragging && openTaskDetails(task.uuid)}
                        >
                            {#if task.assignee}
                                <UserProfilePicture
                                    pictureProps={{
                                        url: task.assignee.profilePicture,
                                        size: 44,
                                    }}
                                />
                            {/if}
                            <div
                                class="mr-3 flex max-h-full flex-col overflow-y-hidden"
                            >
                                <div class="mb-2 flex space-x-1">
                                    {#each task.labels as label}
                                        <div
                                            style={`--color:${
                                                getColorFromInx(label.color)
                                                    .style
                                            };`}
                                            class="label-dot h-2 w-2 rounded-full"
                                        />
                                    {/each}
                                </div>
                                {#if task.deadline}
                                    <div class="flex items-center">
                                        <span class="text-xs"
                                            >Date {dateStringToLocal(
                                                task.deadline
                                            )}</span
                                        >
                                    </div>
                                {/if}
                                <div class="title font-bold">
                                    <span>{task.title}</span>
                                </div>
                            </div>
                        </div>
                    {/each}
                    {#if !isDragging}
                        <div
                            class="add-item ignore-elements hover:ring"
                            on:click={() => openNewTask(section.uuid)}
                        >
                            <div
                                class="flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-full border-2 border-dashed border-primary text-primary"
                            >
                                <IconPlus />
                            </div>
                            <div
                                class="flex max-h-full flex-col overflow-y-hidden font-bold text-primary"
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
    .item,
    .add-item {
        @apply m-2 flex cursor-pointer items-center space-x-4 overflow-y-hidden rounded-lg border border-base-300 bg-base-100 py-4 px-6;
    }

    .content {
        &.layout-grid {
            @apply grid;
            grid-auto-flow: row dense;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            .item,
            .add-item {
                @apply h-24;
                .title {
                    @apply grid;
                    span {
                        @apply overflow-hidden text-ellipsis whitespace-nowrap;
                    }
                }
            }
        }
        &.layout-list {
            @apply flex flex-col;
        }
    }
</style>
