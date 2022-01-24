<script lang="ts">
    import BoardSection from "./board-section.svelte";
    import {
        Mutation_AddWorkspaceBoardSection,
        Query_DashboardBoard,
        Subscription_OnWorkspaceBoardChange,
    } from "$lib/graphql/operations";
    import { query, subscribe } from "svelte-apollo";
    import IconPlus from "../icons/icon-plus.svelte";
    import { getModal } from "../dialogModal.svelte";
    import { client } from "$lib/graphql/client";

    export let boardUUID = null;

    let res = null;
    let subRes = null;
    let board = null;
    let sections = [];

    $: {
        if (boardUUID) {
            res = query(Query_DashboardBoard, {
                variables: { uuid: boardUUID },
            });
            subRes = subscribe(Subscription_OnWorkspaceBoardChange, {
                variables: { uuid: boardUUID },
            });
        }
    }

    $: {
        if (res && $res.data) {
            board = $res.data["workspaceBoard"];
            sections = board["sections"];
        }
    }

    let autoSubscribe = $subRes;

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
</script>

{#if board}
    <div class="flex grow flex-col">
        <!-- Tile -->
        <div class="flex flex-row items-center px-4 py-4">
            <h1 class="font-bold text-3xl grow">{board.title}</h1>
            <div
                class="bg-primary flex items-center p-1 px-3 rounded-lg text-primary-content"
            >
                <span class="text-xs p-1">Deadline</span>
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
        <div class="flex flex-col grow p-2">
            {#each sections as section, index}
                <BoardSection {section} {index} />
            {/each}
            <div
                class="bg-base-100 text-primary m-2 p-5 flex space-x-4 font-bold children-first:bg-debug hover:ring hover:cursor-pointer"
                on:click={() => onAddNewSection()}
            >
                <IconPlus />
                <div>New Section</div>
            </div>
        </div>
    </div>
{/if}
