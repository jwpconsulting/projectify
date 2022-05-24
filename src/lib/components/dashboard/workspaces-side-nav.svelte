<script lang="ts">
    import { query } from "svelte-apollo";
    import { Query_DashboardWorkspacesSideNav } from "$lib/graphql/operations";
    import IconPlus from "../icons/icon-plus.svelte";
    import { gotoDashboard, getDashboardURL } from "$lib/stores/dashboard";
    import ProfilePicture from "../profilePicture.svelte";
    import { goto } from "$app/navigation";

    export let selectedWorkspaceUUID;

    let res = query(Query_DashboardWorkspacesSideNav);
    let workspaces = [];

    export let selectedWorkspace;

    $: {
        if ($res.data) {
            workspaces = $res.data["workspaces"];
            if (!selectedWorkspaceUUID && workspaces.length) {
                gotoDashboard(workspaces[0]["uuid"]);
            } else {
                selectedWorkspace = workspaces
                    ? workspaces.find((w) => w.uuid === selectedWorkspaceUUID)
                    : null;

                if (!selectedWorkspace && workspaces.length) {
                    goto("/error/workspace-not-found");
                }
            }
        }
    }
</script>

<nav
    class="sticky top-0 flex h-full max-h-full shrink-0 flex-col items-center overflow-y-auto bg-base-100 p-2"
>
    {#if workspaces}
        {#each workspaces as workspace (workspace.uuid)}
            <a
                class="btn btn-outline btn-primary btn-square overflow-hidden"
                class:btn-active={workspace.uuid == selectedWorkspaceUUID}
                href={getDashboardURL(workspace.uuid)}
            >
                <ProfilePicture
                    size={48}
                    url={workspace.picture}
                    typogram={workspace.title}
                    emptyIcon={null}
                />
            </a>
        {/each}
        <button class="plus btn btn-outline btn-primary text-primary"
            ><IconPlus /></button
        >
    {/if}
</nav>

<style lang="scss">
    nav > * {
        @apply m-2;
    }
    button {
        @apply h-12 w-12 border-base-300 p-0 text-base-content;
    }
    button.plus {
        @apply text-primary;
    }
    button.plus:hover {
        @apply text-primary-content;
    }

    a.btn-active {
        @apply border-primary bg-base-100 ring;
    }
    a.btn-active:hover {
        @apply bg-primary-focus;
    }
</style>
