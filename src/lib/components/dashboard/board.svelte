<script lang="ts">
    import BoardSection from "./board-section.svelte";
    import {
        Mutation_AddWorkspaceBoardSection,
        Mutation_ArchiveWorkspaceBoard,
        Mutation_DeleteWorkspaceBoard,
        Mutation_MoveWorkspaceBoardSection,
        Mutation_UpdateWorkspaceBoard,
    } from "$lib/graphql/operations";
    import IconPlus from "../icons/icon-plus.svelte";
    import { getModal } from "../dialogModal.svelte";
    import { client } from "$lib/graphql/client";
    import { getWorkspaceBoard } from "$lib/repository";
    import { _ } from "svelte-i18n";
    import { sortable } from "$lib/actions/sortable";
    import delay from "delay";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import ToolBar from "./toolBar.svelte";
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import {
        currentBoardSections,
        filterSectionsTasks,
        gotoDashboard,
        openTaskDetails,
        searchTasks,
    } from "$lib/stores/dashboard";

    import { dateStringToLocal } from "$lib/utils/date";
    import BoardSectionLayoutSelector from "./board-section-layout-selector.svelte";
    import BoardSearchBar from "./board-search-bar.svelte";
    import BoardTaskItem from "./board-task-item.svelte";
    import Loading from "../loading.svelte";
    import {
        dashboardSectionsLayout,
        filterUser,
    } from "$lib/stores/dashboard-ui";
    import IconArrowLeft from "../icons/icon-arrow-left.svelte";
    import IconArrowRight from "../icons/icon-arrow-right.svelte";
    import type { WSSubscriptionStore } from "$lib/stores/wsSubscription";
    import type {
        Label,
        Task,
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types";

    export let workspaceUUID: string | null;
    export let boardUUID: string | null = null;

    let res: WorkspaceBoard | null = null;
    let loading = true;
    let board: WorkspaceBoard | null = null;
    let sections: WorkspaceBoardSection[] = [];
    let isDragging = false;

    let boardWSStore: WSSubscriptionStore | null;

    let filteredSections: WorkspaceBoardSection[] = [];
    let filterLabels: Label[] = [];

    let searchText = "";
    let tasksSearchResults: Task[] = [];

    $: {
        currentBoardSections.set(sections);
    }

    async function fetchBoard() {
        if (!boardUUID) {
            throw new Error("Expected boardUUID");
        }
        res = await getWorkspaceBoard(boardUUID);
        loading = false;
    }

    const refetch = debounce(() => {
        fetchBoard();
    }, 100);

    $: {
        if (boardUUID) {
            fetchBoard();
            boardWSStore = getSubscriptionForCollection(
                "workspace-board",
                boardUUID
            );
        }
    }

    $: {
        if ($boardWSStore) {
            refetch();
        }
    }

    $: {
        if (res) {
            board = res;
            if (board["workspace_board_sections"]) {
                sections = board["workspace_board_sections"];
            }
        }
    }

    $: {
        if (filterLabels.length || $filterUser) {
            filteredSections = filterSectionsTasks(
                sections,
                filterLabels,
                $filterUser
            );
        } else {
            filteredSections = sections;
        }

        if (searchText) {
            tasksSearchResults = searchTasks(filteredSections, searchText);
        }
    }

    async function onAddNewSection() {
        let modalRes = await getModal("newBoardSectionModal").open();
        if (modalRes?.confirm) {
            try {
                const newSection = {
                    title: modalRes.outputs.title,
                    description: "",
                };
                await client.mutate({
                    mutation: Mutation_AddWorkspaceBoardSection,
                    variables: {
                        input: {
                            workspaceBoardUuid: boardUUID,
                            ...newSection,
                        },
                    },
                    optimisticResponse: {
                        addWorkspaceBoardSection: {
                            uuid: "temp-id",
                            __typename: "WorkspaceBoardSection",
                            ...newSection,
                            created: "",
                            tasks: [],
                        },
                    },
                });
            } catch (error) {
                console.error(error);
            }
        }
    }

    async function sectionDragStart() {
        isDragging = true;
    }

    async function sectionDragEnd({
        detail,
    }: {
        detail: { oldIndex: number; newIndex: number };
    }) {
        await delay(10);
        isDragging = false;

        if (detail.oldIndex == detail.newIndex) {
            return;
        }

        let section = sections[detail.oldIndex];
        const order = detail.newIndex;

        if (section) {
            moveSection(section.uuid, order);
        }
    }

    async function moveSection(
        workspaceBoardSectionUuid: string,
        order: number
    ) {
        try {
            await client.mutate({
                mutation: Mutation_MoveWorkspaceBoardSection,
                variables: {
                    input: {
                        workspaceBoardSectionUuid,
                        order,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onEdit() {
        if (!board) {
            throw new Error("Expected board");
        }
        let modalRes = await getModal("editBoardModal").open(board);

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_UpdateWorkspaceBoard,
                variables: {
                    input: {
                        uuid: board.uuid,
                        title: modalRes.outputs.title,
                        deadline: modalRes.outputs.deadline,
                        description: "",
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
    }

    async function onArchive() {
        let modalRes = await getModal("archiveBoardConfirmModal").open();

        if (!modalRes) {
            return;
        }

        if (!board) {
            throw new Error("Expected board");
        }

        try {
            await client.mutate({
                mutation: Mutation_ArchiveWorkspaceBoard,
                variables: {
                    input: {
                        uuid: board.uuid,
                        archived: true,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
        if (!workspaceUUID) {
            throw new Error("Expected workspaceUUID");
        }
        gotoDashboard(workspaceUUID);
    }
    async function onDelete() {
        let modalRes = await getModal("deleteBoardConfirmModal").open();

        if (!modalRes) {
            return;
        }

        if (!board) {
            throw new Error("Expected board");
        }

        try {
            await client.mutate({
                mutation: Mutation_DeleteWorkspaceBoard,
                variables: {
                    input: {
                        uuid: board.uuid,
                    },
                },
            });
        } catch (error) {
            console.error(error);
        }
        if (!workspaceUUID) {
            throw new Error("Expected workspaceUUID");
        }
        gotoDashboard(workspaceUUID);
    }

    let sectionContainerEl: HTMLElement | null = null;
    let scrollInx = 0;

    function onSectionScroll(_e: Event) {
        if (!sectionContainerEl) {
            throw new Error("Expected sectionContainerEl");
        }
        const s = sectionContainerEl.scrollLeft;
        const vw = sectionContainerEl.clientWidth;

        let dist = Number.MAX_SAFE_INTEGER;
        sectionContainerEl
            .querySelectorAll(":scope > div")
            .forEach((el: Element, inx: number) => {
                if (!(el instanceof HTMLElement)) {
                    throw new Error("Expected HTMLElement");
                }
                let newDist = Math.abs(
                    el.offsetLeft + el.clientWidth / 2 - (s + vw / 2)
                );
                if (newDist < dist) {
                    dist = newDist;
                    scrollInx = inx;
                }
            });
    }

    function scrollNext() {
        scrollToInx(scrollInx + 1);
    }

    function scrollPrev() {
        scrollToInx(scrollInx - 1);
    }

    function scrollToInx(inx: number) {
        if (!sectionContainerEl) {
            throw new Error("Expected sectionContainerEl");
        }
        const w = sectionContainerEl.clientWidth;
        const el: HTMLElement | null = sectionContainerEl.querySelector(
            `:scope > div:nth-child(${inx + 1})`
        );
        if (el) {
            sectionContainerEl.scrollTo({
                left: el.offsetLeft - w / 2 + el.clientWidth / 2,
                behavior: "smooth",
            });
        } else {
            throw new Error("Could not find el");
        }
        console.log("scroll to inx", scrollInx, inx);
    }

    let sectionToolTipHoverInx = 0;
    $: sectionTollTipLabel = filteredSections[sectionToolTipHoverInx]?.title;

    function onSwitchWithPrevSection({
        detail: { section },
    }: {
        detail: { section: WorkspaceBoardSection };
    }) {
        const sectionIndex = sections.findIndex((s) => s.uuid == section.uuid);
        const prevSection = sections[sectionIndex - 1];

        if (prevSection) {
            moveSection(section.uuid, prevSection._order);
        }
    }
    function onSwitchWithNextSection({
        detail: { section },
    }: {
        detail: { section: WorkspaceBoardSection };
    }) {
        const sectionIndex: number = sections.findIndex(
            (s: WorkspaceBoardSection) => s.uuid == section.uuid
        );
        const nextSection: WorkspaceBoardSection | null =
            sections[sectionIndex + 1] || null;

        if (nextSection) {
            moveSection(section.uuid, nextSection._order);
        }
    }
</script>

{#if loading}
    <div class="flex grow flex-col items-center justify-center bg-base-200">
        <Loading />
    </div>
{:else if board}
    <div
        class="relative flex h-full min-h-full grow flex-col overflow-hidden bg-base-200"
    >
        <header
            class="flex flex-col space-y-4 border-b border-base-300 bg-base-100"
        >
            <!-- Tile -->
            <div class="flex flex-row items-center space-x-2 px-4 pt-4">
                <div class="grid shrink grow basis-0 text-3xl font-bold">
                    <span class="nowrap-ellipsis">{board.title}</span>
                </div>
                <BoardSectionLayoutSelector />
                {#if board.workspace_board_sections}
                    <ToolBar
                        items={[
                            {
                                label: $_("Edit"),
                                icon: IconEdit,
                                onClick: onEdit,
                            },
                            {
                                label: $_("Archive"),
                                icon: IconTrash,
                                onClick: onArchive,
                                hidden:
                                    board.workspace_board_sections.length == 0,
                            },
                            {
                                label: $_("Delete"),
                                icon: IconTrash,
                                onClick: onDelete,
                                hidden:
                                    board.workspace_board_sections.length > 0,
                            },
                        ]}
                    />
                {/if}
                {#if board.deadline}
                    <div
                        class="flex shrink-0 items-center rounded-lg bg-primary p-1 px-3 text-primary-content"
                    >
                        <span class="p-1 text-xs">{$_("deadline")}</span>
                        <span class="p-1 text-base "
                            >{dateStringToLocal(board.deadline)}</span
                        >
                    </div>
                {/if}
            </div>

            <div class="flex grow items-stretch">
                <BoardSearchBar
                    bind:searchText
                    bind:filterLabels
                    bind:filterUser={$filterUser}
                />
            </div>
        </header>

        {#if searchText}
            <!-- Flat Tasks Results -->
            {#if tasksSearchResults.length}
                <div class="flex grow flex-col overflow-y-auto p-2">
                    {#each tasksSearchResults as task}
                        <BoardTaskItem
                            {task}
                            on:click={() => openTaskDetails(task.uuid)}
                        />
                    {/each}
                </div>
            {:else}
                <div class="flex grow items-center justify-center">
                    <div class="rounded-md bg-base-100 p-6 shadow-sm">
                        {$_("tasks-not-found-for")} "{searchText}"
                    </div>
                </div>
            {/if}
        {:else}
            <!-- Sections -->
            <div
                on:scroll={onSectionScroll}
                bind:this={sectionContainerEl}
                class={"flex p-2 " +
                    ($dashboardSectionsLayout == "columns"
                        ? "section-layout-col"
                        : "section-layout-row")}
                use:sortable={{ group: "Sections", draggable: ".section" }}
                on:dragStart={sectionDragStart}
                on:dragEnd={sectionDragEnd}
            >
                {#each filteredSections as section, index (section.uuid)}
                    <BoardSection
                        {section}
                        isFirst={index == 0}
                        isLast={index == filteredSections.length - 1}
                        bind:isDragging
                        on:switchWithPrevSection={onSwitchWithPrevSection}
                        on:switchWithNextSection={onSwitchWithNextSection}
                    />
                {/each}
                {#if !isDragging}
                    <div
                        class="ignore-elements m-2 flex shrink-0 space-x-4 bg-base-100 p-5 font-bold text-primary shadow-sm hover:cursor-pointer hover:ring"
                        on:click={() => onAddNewSection()}
                    >
                        <IconPlus />
                        <div>{$_("new-section")}</div>
                    </div>
                {/if}
            </div>
            {#if $dashboardSectionsLayout == "columns"}
                <div
                    class="pagination-controls absolute inset-0 top-[120px] flex items-center justify-center gap-4 px-4 py-1 pb-6"
                >
                    <button
                        on:click={scrollPrev}
                        class="diraction-btn btn btn-primary btn-circle shadow-sm"
                        class:invisible={scrollInx <= 0}
                    >
                        <div class="translate-x-1">
                            <IconArrowLeft />
                        </div>
                    </button>
                    <div
                        class="flex grow items-center justify-center self-end"
                    >
                        <div
                            class="pagination-dots w relative flex justify-center gap-2 "
                        >
                            <div
                                class="section-tooltip"
                                style={`--pos-factor: ${
                                    sectionToolTipHoverInx /
                                    (filteredSections.length - 1)
                                }`}
                            >
                                {sectionTollTipLabel}
                            </div>
                            {#each filteredSections as section, index (section.uuid)}
                                <div
                                    on:click={() => scrollToInx(index)}
                                    on:mouseover={() =>
                                        (sectionToolTipHoverInx = index)}
                                    on:focus={() =>
                                        (sectionToolTipHoverInx = index)}
                                    class:active={scrollInx == index}
                                    class="relative flex h-4 w-4 cursor-pointer select-none items-center justify-center rounded-full bg-primary bg-opacity-30 p-1 text-sm shadow-sm hover:bg-opacity-50"
                                >
                                    <div
                                        class="absolute inset-0 rounded-full bg-primary"
                                    />
                                </div>
                            {/each}
                        </div>
                    </div>
                    <button
                        on:click={scrollNext}
                        class="diraction-btn btn btn-primary btn-square rounded-full shadow-sm"
                        class:invisible={scrollInx >= filteredSections.length}
                    >
                        <div class="-translate-x-1">
                            <IconArrowRight />
                        </div>
                    </button>
                </div>
            {/if}
        {/if}
    </div>
{/if}

<style lang="scss">
    .section-layout-row {
        @apply grow flex-col overflow-y-auto;
    }

    :global(.section-layout-col) {
        @apply grow flex-row items-start justify-start overflow-x-auto;
        @apply pb-10;
        @apply snap-x snap-proximity;
    }

    :global(.section-layout-col > *) {
        --scroll-padding: 138px;
        flex-shrink: 0;
        width: calc(70% - var(--scroll-padding));
        min-width: 400px;
        max-width: 800px;

        scroll-snap-align: center;
        &:first-child {
            margin-left: calc(50% - var(--scroll-padding) * 2);
        }
    }

    .pagination-dots {
        @apply relative select-none;
        > * {
            transition: all ease-in-out 300ms;
            > * {
                transform: scale(0.5);
                transition: all ease-in-out 300ms;
            }
            &.active {
                > * {
                    transform: scale(1);
                }
            }
        }

        > .section-tooltip {
            @apply absolute whitespace-nowrap rounded-full bg-primary-content px-3 py-1 text-xs uppercase text-primary;
            @apply top-[-32px];

            @apply flex items-center justify-center;
            opacity: 0;
            flex-shrink: 0;

            transform: translateX(calc(-50%));
            left: calc(var(--pos-factor) * (100% - 16px) + 8px);

            transition: all ease-out 200ms;
            filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));

            &::before {
                content: "";
                position: absolute;
                bottom: -4px;

                width: 0;
                height: 0;
                border-style: solid;
                border-width: 4px 4px 0 4px;
                border-color: hsla(var(--pc) / 1) transparent transparent
                    transparent;
            }
        }

        &:hover {
            > .section-tooltip {
                opacity: 1;
            }
        }
    }
    .pagination-controls {
        pointer-events: none;
        > * {
            pointer-events: all;
        }

        > .diraction-btn {
            box-shadow: 0 0 0 8px hsla(var(--p) / 0.1),
                0 3px 8px 0 hsla(var(--p) / 0.3);

            transition: all ease-in-out 100ms;
            &.invisible {
                visibility: visible;
                opacity: 0;
                transform: scale(0.7);
                pointer-events: none;
            }
        }
    }
</style>
