<script lang="ts">
    import { query } from "svelte-apollo";
    import { Query_DashboardWorkspacesSideNav } from "$lib/graphql/queries";
    import IconPlus from "../icons/icon-plus.svelte";

    export let selectedWorkspaceUUID;

    let res = query(Query_DashboardWorkspacesSideNav);
    let workspaces = [];

    $: {
        if ($res.data) {
            workspaces = $res.data["workspaces"];
            if (!selectedWorkspaceUUID && workspaces.length) {
                selectedWorkspaceUUID = workspaces[0]["uuid"];
            }
        }
    }

    function workspaceIconFrom(title) {
        return title.substr(0, 2);
    }
</script>

<nav class="bg-neutral-content flex flex-col w-24 items-center p-2">
    {#if workspaces}
        {#each workspaces as workspace (workspace.uuid)}
            <button
                class="btn btn-primary btn-outline"
                class:btn-active={workspace.uuid == selectedWorkspaceUUID}
                on:click={() => (selectedWorkspaceUUID = workspace.uuid)}
                >{workspaceIconFrom(workspace.title)}</button
            >
        {/each}
        <button class="plus btn btn-primary btn-outline text-primary"
            ><IconPlus /></button
        >
    {/if}
</nav>

<style lang="scss">
    nav > * {
        @apply m-2;
    }
    button {
        @apply w-12 h-12 border-base-300 p-0 text-base-content;
    }
    button.btn-active:hover {
        @apply bg-primary-focus text-base-content;
    }
    button.plus {
        @apply text-primary;
    }
    button.btn-active {
        @apply bg-neutral-content border-2 border-primary;
    }
</style>
