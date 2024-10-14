<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Briefcase } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { selectWorkspaceUuid } from "$lib/stores/dashboard/ui";
    import type { WorkspaceDetail } from "$lib/types/workspace";
    import { getDashboardWorkspaceUrl } from "$lib/urls";

    export let workspaces: Pick<WorkspaceDetail, "title" | "uuid">[];
</script>

<Layout>
    <p class="px-4 py-2 font-bold">
        {$_("overlay.context-menu.workspace.select-workspace")}
    </p>
    {#each workspaces as workspace}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getDashboardWorkspaceUrl(workspace),
                onInteract: () => selectWorkspaceUuid(workspace.uuid),
            }}
            label={workspace.title}
            icon={Briefcase}
        />
    {/each}
</Layout>
