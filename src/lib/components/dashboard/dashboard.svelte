<script lang="ts">
    import WorkspacesSideNav from "$lib/components/dashboard/workspaces-side-nav.svelte";
    import BoardsSideNav from "$lib/components/dashboard/boards-side-nav.svelte";
    import Board from "./board.svelte";
    import IconSettings from "../icons/icon-settings.svelte";
    import DrawerModal from "../drawerModal.svelte";
    import TaskDetails from "./task-details.svelte";

    let selectedWorkspaceUUID = null;
    let selectedBoardUUID = null;
</script>

<main class="page p-0 flex-row divide-x divide-base-300 max-h-screen">
    <!-- First side bar -->
    <WorkspacesSideNav bind:selectedWorkspaceUUID />

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
            <BoardsSideNav {selectedWorkspaceUUID} bind:selectedBoardUUID />
        </div>

        <!-- User infos -->
        <div class="flex p-3 sticky bottom-0">
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

    <Board bind:boardUUID={selectedBoardUUID} />

    <DrawerModal>
        <TaskDetails />
    </DrawerModal>
</main>
