<script lang="ts">
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import {
        currentWorkspace,
        currentWorkspaces,
    } from "$lib/stores/dashboard";

    $: workspaces = $currentWorkspaces ?? [];
    $: workspace = $currentWorkspace;
</script>

<div class="flex h-full grow flex-row">
    <!-- this breakpoint is in tune with the mobile menu breakpoint -->
    <div class="hidden lg:block">
        <SideNav {workspaces} {workspace} />
    </div>
    <div class="grow">
        <slot />
    </div>
</div>
