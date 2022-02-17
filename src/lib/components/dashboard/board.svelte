<script lang="ts">
    import BoardSection from "./board-section.svelte";
    import {
        Mutation_AddWorkspaceBoardSection,
        Mutation_MoveWorkspaceBoardSection,
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

    export let boardUUID = null;

    let res = null;
    let board = null;
    let sections = [];
    let isDragging = false;

    let boardWSStore;

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

    async function onAddNewSection() {
        let modalRes = await getModal("newBoardSectionModal").open();
        if (modalRes) {
            try {
                const newSection = {
                    title: modalRes.title,
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
                            workspaceBoardSection: {
                                uuid: "temp-id",
                                __typename: "WorkspaceBoardSection",
                                ...newSection,
                                created: "",
                                tasks: [],
                            },
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

    function onEdit() {
        console.log("edit");
    }
    function onArchive() {
        console.log("archive");
    }
    function onDelete() {
        console.log("delete");
    }
</script>

{#if res && $res.loading}
    <div class="flex grow flex-col items-center justify-center">
        {$_("loading")}
    </div>
{:else if board}
    <div class="flex grow flex-col">
        <!-- Tile -->
        <div class="flex flex-row items-center px-4 py-4 gap-2">
            <div class="grid font-bold text-3xl grow shrink basis-0">
                <span class="nowrap-ellipsis">{board.title}</span>
            </div>
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
            <div
                class="bg-primary flex items-center p-1 px-3 rounded-lg text-primary-content shrink-0"
            >
                <span class="text-xs p-1">{$_("deadline")}</span>
                <span class="text-base p-1 ">2021.12.31</span>
            </div>
        </div>

        <!-- Tags -->
        <div class="flex px-3 flex-wrap">
            {#each ["All", "Manager", "Design", "Engineer", "Marketing", "Other", "My task"] as tag}
                <div
                    class="whitespace-nowrap font-bold text-xs bg-base-100 px-3 py-1 m-1 rounded-full border border-base-300"
                >
                    {tag}
                </div>
            {/each}
        </div>

        <!-- Sections -->
        <div
            class="flex flex-col grow p-2"
            use:sortable={{ group: "Sections" }}
            on:dragStart={sectionDragStart}
            on:dragEnd={sectionDragEnd}
        >
            {#each sections as section, index (section.uuid)}
                <BoardSection
                    {section}
                    {index}
                    boardUUID={board.uuid}
                    bind:isDragging
                />
            {/each}
            {#if !isDragging}
                <div
                    class="ignore-elements bg-base-100 text-primary m-2 p-5 flex space-x-4 font-bold children-first:bg-debug hover:ring hover:cursor-pointer"
                    on:click={() => onAddNewSection()}
                >
                    <IconPlus />
                    <div>{$_("new-section")}</div>
                </div>
            {/if}
        </div>
    </div>
{/if}
