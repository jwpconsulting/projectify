<script lang="ts">
    import BoardSection from "./board-section.svelte";
    import {
        Mutation_AddWorkspaceBoardSection,
        Mutation_ArchiveWorkspaceBoard,
        Mutation_DeleteWorkspaceBoard,
        Mutation_MoveWorkspaceBoardSection,
        Mutation_UpdateWorkspaceBoard,
        Query_DashboardBoard,
    } from "$lib/graphql/operations";
    import { query } from "svelte-apollo";
    import IconPlus from "../icons/icon-plus.svelte";
    import { getModal } from "../dialogModal.svelte";
    import { client } from "$lib/graphql/client";
    import { _ } from "svelte-i18n";
    import { sortable } from "$lib/actions/sortable";
    import delay from "delay";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import ToolBar from "./toolBar.svelte";
    import IconEdit from "../icons/icon-edit.svelte";
    import IconTrash from "../icons/icon-trash.svelte";
    import {
        filterSectionsTaskWithLabels,
        gotoDashboard,
    } from "$lib/stores/dashboard";
    import LabelPillList from "./labelList.svelte";
    import { currentWorkspaceLabels } from "$lib/stores/dashboard";
    import { dateStringToLocal } from "$lib/utils/date";
    import BoardSectionLayoutSelector from "./board-section-layout-selector.svelte";

    export let workspaceUUID;
    export let boardUUID = null;

    let res = null;
    let board = null;
    let sections = [];
    let isDragging = false;

    let boardWSStore;

    let filteredSections = [];
    let filterLabels = [];

    const refetch = debounce(() => {
        res.refetch();
    }, 100);

    $: {
        if (boardUUID) {
            res = query(Query_DashboardBoard, {
                variables: { uuid: boardUUID },
                fetchPolicy: "network-only",
            });

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
        if (res && $res.data) {
            board = $res.data["workspaceBoard"];
            if (board["sections"]) {
                sections = board["sections"];
            }
        }
    }

    $: {
        if (filterLabels.length) {
            filteredSections = filterSectionsTaskWithLabels(
                sections,
                filterLabels
            );
        } else {
            filteredSections = sections;
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
                let mRes = await client.mutate({
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

    async function sectionDragEnd({ detail }) {
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

    async function moveSection(workspaceBoardSectionUuid, order) {
        try {
            let mRes = await client.mutate({
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
        let modalRes = await getModal("editBoardModal").open(board);

        if (!modalRes) {
            return;
        }

        try {
            let mRes = await client.mutate({
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

        try {
            let mRes = await client.mutate({
                mutation: Mutation_ArchiveWorkspaceBoard,
                variables: {
                    input: {
                        uuid: board.uuid,
                        archived: true,
                    },
                },
                update(cache, { data }) {
                    cache.modify({
                        id: `Workspace:${workspaceUUID}`,
                        fields: {
                            boards(list = []) {
                                return list.filter(
                                    (it) =>
                                        it.__ref !=
                                        `WorkspaceBoard:${board.uuid}`
                                );
                            },
                        },
                    });
                },
            });

            gotoDashboard(workspaceUUID);
        } catch (error) {
            console.error(error);
        }
    }
    async function onDelete() {
        let modalRes = await getModal("deleteBoardConfirmModal").open();

        if (!modalRes) {
            return;
        }

        try {
            let mRes = await client.mutate({
                mutation: Mutation_DeleteWorkspaceBoard,
                variables: {
                    input: {
                        uuid: board.uuid,
                    },
                },
                update(cache, { data }) {
                    cache.modify({
                        id: `Workspace:${workspaceUUID}`,
                        fields: {
                            boards(list = []) {
                                return list.filter(
                                    (it) =>
                                        it.__ref !=
                                        `WorkspaceBoard:${board.uuid}`
                                );
                            },
                        },
                    });
                },
            });

            gotoDashboard(workspaceUUID);
        } catch (error) {
            console.error(error);
        }
    }
</script>

{#if res && $res.loading}
    <div class="flex grow flex-col items-center justify-center bg-base-200">
        {$_("loading")}
    </div>
{:else if board}
    <div
        class="flex grow flex-col bg-base-200 h-full min-h-full overflow-hidden"
    >
        <header
            class="flex flex-col bg-base-100 pb-6 border-b border-base-300"
        >
            <!-- Tile -->
            <div class="flex flex-row items-center px-4 py-4 gap-2">
                <div class="grid font-bold text-3xl grow shrink basis-0">
                    <span class="nowrap-ellipsis">{board.title}</span>
                </div>
                <BoardSectionLayoutSelector />
                <ToolBar
                    items={[
                        { label: $_("Edit"), icon: IconEdit, onClick: onEdit },
                        {
                            label: $_("Archive"),
                            icon: IconTrash,
                            onClick: onArchive,
                            hidden: !board?.sections?.length,
                        },
                        {
                            label: $_("Delete"),
                            icon: IconTrash,
                            onClick: onDelete,
                            hidden: board?.sections?.length,
                        },
                    ]}
                />
                {#if board.deadline}
                    <div
                        class="bg-primary flex items-center p-1 px-3 rounded-lg text-primary-content shrink-0"
                    >
                        <span class="text-xs p-1">{$_("deadline")}</span>
                        <span class="text-base p-1 "
                            >{dateStringToLocal(board.deadline)}</span
                        >
                    </div>
                {/if}
            </div>

            <!-- Labels -->
            <div class="px-4 inline-flex gap-2 flex-wrap">
                <LabelPillList
                    editable={true}
                    labels={$currentWorkspaceLabels}
                    bind:selectedLabels={filterLabels}
                />
            </div>
        </header>

        <!-- Sections -->
        <div
            class="flex flex-col grow p-2 overflow-y-auto"
            use:sortable={{ group: "Sections", draggable: ".section" }}
            on:dragStart={sectionDragStart}
            on:dragEnd={sectionDragEnd}
        >
            {#each filteredSections as section, index (section.uuid)}
                <BoardSection
                    {section}
                    {index}
                    boardUUID={board.uuid}
                    bind:isDragging
                />
            {/each}
            {#if !isDragging}
                <div
                    class="ignore-elements bg-base-100 text-primary m-2 p-5 flex space-x-4 font-bold hover:ring hover:cursor-pointer"
                    on:click={() => onAddNewSection()}
                >
                    <IconPlus />
                    <div>{$_("new-section")}</div>
                </div>
            {/if}
        </div>
    </div>
{/if}
