<script lang="ts">
    import Collapsed from "$lib/figma/navigation/side-nav/Collapsed.svelte";
    import Full from "$lib/figma/navigation/side-nav/Full.svelte";
    import { sideNavOpen } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[];
    export let workspace: Workspace;
</script>

{#if $sideNavOpen}
    <div class="max-w-xs 2xl:max-w-md">
        <Full {workspaces} {workspace} />
    </div>
{:else}
    <!-- Figma says 72px but we only have 64 or 80 (16, 29 rem respectively)-->
    <!-- Might we refactor this into something separate? -->
    <div class="w-20">
        <Collapsed {workspace} {workspaces} />
    </div>
{/if}
