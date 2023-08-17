<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Briefcase, Plus } from "@steeze-ui/heroicons";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import { getDashboardWorkspaceUrl } from "$lib/urls";
    import type { Workspace } from "$lib/types/workspace";

    export let workspaces: Workspace[];
</script>

{#each workspaces as workspace}
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
