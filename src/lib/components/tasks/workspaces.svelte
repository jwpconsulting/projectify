<script lang="ts">
    import WorkspacesSideNav from "$lib/components/tasks/workspaces-side-nav.svelte";
    import BoardsSideNav from "$lib/components/tasks/boards-side-nav.svelte";

    import { user } from "$lib/stores/user";

    import { query } from "svelte-apollo";
    import { Query_TaskPage } from "$lib/grapql/queries";

    import IconSettings from "../icons/icon-settings.svelte";
    const res = query(Query_TaskPage);
</script>

{#if $res.loading}
    <main class="page page-center">Loading...</main>
{:else if $res.error}
    <main class="page page-center">Error: {$res.error["message"]}</main>
{:else}
    <main class="page p-0 flex-row divide-x divide-border-1">
        <WorkspacesSideNav workspaces={$res.data["workspaces"]} />
        <nav class="side-nav-2">
            <div>
                <h1>Projectify</h1>
                <button class="btn btn-outline btn-circle btn-xs">
                    <IconSettings />
                </button>
            </div>
            <BoardsSideNav boards={$res.data["workspaces"][0]["boards"]} />
            <div class="user-info">
                <div class="description">Interface Designer & Fr...</div>
                <div class="icon" />
                <div class="name">{$user.email}</div>
            </div>
        </nav>
        <div />
    </main>
{/if}

<style lang="scss">
    .side-nav-2 {
        @apply bg-wite-1 w-60;
    }
</style>
