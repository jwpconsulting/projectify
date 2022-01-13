<script lang="ts">
    import WorkspacesSideNav from "$lib/components/dashboard/workspaces-side-nav.svelte";
    import BoardsSideNav from "$lib/components/dashboard/boards-side-nav.svelte";

    import { user } from "$lib/stores/user";

    import { query } from "svelte-apollo";
    import { Query_TaskPage } from "$lib/grapql/queries";

    import IconSettings from "../icons/icon-settings.svelte";

    import BoardSection from "./board-section.svelte";

    const res = query(Query_TaskPage);
</script>

{#if $res.loading}
    <main class="page page-center">Loading...</main>
{:else if $res.error}
    <main class="page page-center">Error: {$res.error["message"]}</main>
{:else}
    <main class="page p-0 flex-row divide-x divide-border-1 max-h-screen">
        <!-- First side bar -->
        <WorkspacesSideNav workspaces={$res.data["workspaces"]} />

        <!-- Secon side bar -->
        <nav class="flex flex-col bg-base-100 w-60">
            <!-- Tite and settings -->
            <div class="flex p-4">
                <h1 class="grow font-bold text-xl">Projectify</h1>
                <button class="btn btn-primary btn-outline btn-circle btn-xs">
                    <IconSettings />
                </button>
            </div>

            <!-- Boards nav -->
            <div class="grow">
                <h2 class="p-4 text-base font-bold">Workspace Boards</h2>
                <BoardsSideNav boards={$res.data["workspaces"][0]["boards"]} />
            </div>

            <!-- User infos -->
            <div class="flex p-3">
                <div
                    class="m-1 flex -space-x-1 overflow-hidden w-8 h-8 rounded-full shrink-0"
                >
                    <img
                        width="100%"
                        height="100%"
                        src="https://picsum.photos/200"
                        alt="user"
                    />
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
                        Abraham
                    </div>
                </div>
            </div>
        </nav>

        <!-- Main Content -->
        <div class="flex grow flex-col overflow-y-scroll">
            <!-- Tile -->
            <div class="flex flex-row items-center px-4 py-4">
                <h1 class="font-bold text-3xl grow">Project ver1</h1>
                <div
                    class="bg-blue-2 flex items-center p-1 px-3 rounded-lg text-wite-1"
                >
                    <span class="text-xs p-1">Deadline</span>
                    <span class="text-base p-1 ">2021.12.31</span>
                </div>
            </div>

            <!-- Tags -->
            <div class="flex px-3 flex-wrap">
                {#each ["All", "Manager", "Design", "Engineer", "Marketing", "Other", "My task"] as tag}
                    <div
                        class="whitespace-nowrap font-bold text-xs bg-base-100 px-3 py-1 m-1 rounded-full border border-border-1"
                    >
                        {tag}
                    </div>
                {/each}
            </div>

            <!-- Sections -->
            <div class="flex flex-col grow p-2">
                {#each $res.data["workspaces"][0]["boards"][0]["sections"] as section, index}
                    <BoardSection {section} {index} />
                {/each}
            </div>
        </div>
    </main>
{/if}
