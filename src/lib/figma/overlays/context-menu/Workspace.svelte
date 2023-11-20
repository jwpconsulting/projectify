<script lang="ts">
    import { Briefcase, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { selectWorkspaceUuid } from "$lib/stores/dashboard";
    import type { Workspace } from "$lib/types/workspace";
    import { getDashboardWorkspaceUrl } from "$lib/urls";

    export let workspaces: Workspace[];
</script>

<Layout>
    {#each workspaces as workspace}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getDashboardWorkspaceUrl(workspace.uuid),
                onInteract: () => selectWorkspaceUuid(workspace.uuid),
            }}
            label={workspace.title}
            state="normal"
            icon={Briefcase}
        />
    {/each}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("add new workspace not implemented"),
        }}
        label={$_("overlay.context-menu.workspace.add-new-workspace")}
        state="normal"
        color="primary"
        icon={Plus}
    />
</Layout>
