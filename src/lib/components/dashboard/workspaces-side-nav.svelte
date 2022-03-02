<script lang="ts">
    import { query } from "svelte-apollo";
    import { Query_DashboardWorkspacesSideNav } from "$lib/graphql/operations";
    import IconPlus from "../icons/icon-plus.svelte";
    import { gotoDashboard, getDashboardURL } from "$lib/stores/dashboard";

    export let selectedWorkspaceUUID;

    let res = query(Query_DashboardWorkspacesSideNav);
    let workspaces = [];

    export let selectedWorkspace;

    $: {
        if ($res.data) {
            workspaces = $res.data["workspaces"];
            if (!selectedWorkspaceUUID && workspaces.length) {
                gotoDashboard(workspaces[0]["uuid"]);
            }
        }
    }

    $: {
        selectedWorkspace = workspaces
            ? workspaces.find((w) => w.uuid === selectedWorkspaceUUID)
            : null;
    }

    function workspaceIconFrom(title) {
        return title.substr(0, 2);
    }
</script>

<nav
    class="bg-base-100 shrink-0 flex flex-col items-center p-2 h-full max-h-full sticky top-0 overflow-y-auto"
>
    {#if workspaces}
        {#each workspaces as workspace (workspace.uuid)}
            <a
                class="btn btn-primary btn-outline btn-square"
                class:btn-active={workspace.uuid == selectedWorkspaceUUID}
                href={getDashboardURL(workspace.uuid)}
                >{workspaceIconFrom(workspace.title)}</a
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
    button.plus {
        @apply text-primary;
    }
    button.plus:hover {
        @apply text-primary-content;
    }

    a.btn-active {
        @apply bg-base-100 ring border-primary;
    }
    a.btn-active:hover {
        @apply bg-primary-focus;
    }
</style>
