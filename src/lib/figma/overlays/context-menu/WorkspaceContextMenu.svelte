<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { Briefcase, Plus } from "@steeze-ui/heroicons";
    import { getDashboardWorkspaceUrl } from "$lib/urls";
    import Loading from "$lib/components/loading.svelte";
    import type { WorkspaceSearchModule } from "$lib/types/stores";

    export let workspaceSearchModule: WorkspaceSearchModule;

    let { workspaces, setWorkspaces } = workspaceSearchModule;

    $: {
        // XXX this could be done in a more central location
        if (!$workspaces) {
            setWorkspaces();
        }
    }
</script>

{#if $workspaces}
    {#each $workspaces as workspace}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getDashboardWorkspaceUrl(workspace.uuid),
            }}
            label={workspace.title}
            state="normal"
            icon={Briefcase}
        />
    {/each}
{:else}
    <Loading />
{/if}
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("add new workspace not implemented"),
    }}
    label={$_("workspace-overlay.add-new-workspace")}
    state="normal"
    color="primary"
    icon={Plus}
/>
