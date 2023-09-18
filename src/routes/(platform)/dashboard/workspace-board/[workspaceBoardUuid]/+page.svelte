<script lang="ts">
    import type { PageData } from "./$types";

    import Dashboard from "$lib/components/dashboard/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import {
        currentWorkspace,
        currentWorkspaceBoard,
    } from "$lib/stores/dashboard";

    export let data: PageData;

    let { workspaceBoard, workspace } = data;
    const { workspaces } = data;

    $: workspaceBoard = $currentWorkspaceBoard ?? workspaceBoard;
    $: workspace = $currentWorkspace ?? workspace;
</script>

<div class="flex h-full grow flex-row">
    <!-- this breakpoint is in tune with the mobile menu breakpoint -->
    <div class="hidden lg:block">
        <SideNav {workspaces} {workspace} />
    </div>
    <Dashboard {workspaceBoard} />
</div>
