<script lang="ts">
    import WorkspacesSideNav from "$lib/components/dashboard/workspaces-side-nav.svelte";
    import BoardsSideNav from "$lib/components/dashboard/boards-side-nav.svelte";

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
        <nav class="flex flex-col bg-wite-1 w-60">
            <div class="flex p-4">
                <h1 class="grow font-bold text-xl">Projectify</h1>
                <button class="btn btn-primary btn-outline btn-circle btn-xs">
                    <IconSettings />
                </button>
            </div>
            <div class="grow">
                <h2 class="p-4 text-base font-bold">Workspace Boards</h2>
                <BoardsSideNav boards={$res.data["workspaces"][0]["boards"]} />
            </div>
            <!-- User infos -->
            <div class="flex p-3">
                <div
                    class="m-1 flex -space-x-1 overflow-hidden w-8 h-8 rounded-full shrink-0"
                >
                    <img src="https://fakeimg.pl/64/" alt="user" />
                </div>
                <div class="m-1 overflow-hidden">
                    <div
                        class="text-xs overflow-hidden whitespace-nowrap text-ellipsis"
                    >
                        Interface Designer & Frontend Interface Designer
                    </div>
                    <div
                        class="text-base font-bold overflow-hidden whitespace-nowrap text-ellipsis"
                    >
                        Abraham Abraham Abraham Abraham Abraham Abraham
                    </div>
                </div>
            </div>
        </nav>
        <div />
    </main>
{/if}
