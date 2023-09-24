<script lang="ts">
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import {
        currentWorkspace,
        currentWorkspaces,
    } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    let workspace: Workspace | undefined = undefined;
    let workspaces: Workspace[] = [];

    $: workspaces = $currentWorkspaces ?? [];
    $: workspace = $currentWorkspace;
</script>

<div class="flex h-full grow flex-row">
    <!-- this breakpoint is in tune with the mobile menu breakpoint -->
    <div class="hidden md:block">
        {#if workspace}
            <SideNav {workspaces} {workspace} />
        {:else}
            Loading workspaces
        {/if}
    </div>
    <div class="grow">
        <slot />
    </div>
</div>
