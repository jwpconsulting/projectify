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

<div class="flex min-h-0 shrink grow flex-row">
    <!-- this breakpoint is in tune with the mobile menu breakpoint -->
    <div class="hidden h-full shrink-0 overflow-y-auto md:block">
        {#if workspace}
            <SideNav {workspaces} {workspace} />
        {:else}
            Loading workspaces
        {/if}
    </div>
    <!-- not inserting min-w-0 will mean that this div will extend as much as
    needed around whatever is inside the slot -->
    <div class="min-w-0 grow overflow-y-auto">
        <slot />
    </div>
</div>
