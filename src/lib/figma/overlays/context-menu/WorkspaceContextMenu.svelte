<script lang="ts">
    import { Briefcase, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import { getDashboardWorkspaceUrl } from "$lib/urls";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
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
