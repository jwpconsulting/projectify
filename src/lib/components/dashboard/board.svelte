<script lang="ts">
    import BoardSection from "./board-section.svelte";
    import { Query_DashboardBoard } from "$lib/graphql/queries";
    import { query } from "svelte-apollo";

    export let boardUUID = null;

    let res = null;
    let sections = [];

    $: {
        if (boardUUID) {
            res = query(Query_DashboardBoard, {
                variables: { uuid: boardUUID },
            });
        }
    }

    $: {
        if (res && $res.data) {
            sections = $res.data["workspaceBoard"]["sections"];
        }
    }
</script>

<div class="flex grow flex-col overflow-y-scroll">
    <!-- Tile -->
    <div class="flex flex-row items-center px-4 py-4">
        <h1 class="font-bold text-3xl grow">Project ver1</h1>
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
    </div>
</div>
