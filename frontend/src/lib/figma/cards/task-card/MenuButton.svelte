<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        ProjectDetail,
        ProjectDetailTask,
        ProjectDetailSection,
    } from "$lib/types/workspace";

    export let task: ProjectDetailTask;
    // this is only ever needed for the dashboard, not when a task is part
    // of search results... time for another ADT?
    export let project: ProjectDetail;
    export let section: ProjectDetailSection | undefined = undefined;

    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        const contextMenu: ContextMenuType =
            section === undefined
                ? {
                      kind: "task",
                      task,
                      location: "dashboardSearch",
                      project,
                  }
                : {
                      kind: "task",
                      task,
                      location: "dashboard",
                      section,
                      project,
                  };
        await openContextMenu(contextMenu, dropDownMenuBtnRef);
    }

    const action = { kind: "button" as const, action: openDropDownMenu };
</script>

<div bind:this={dropDownMenuBtnRef}>
    <CircleIcon
        icon="ellipsis"
        size="medium"
        {action}
        ariaLabel={$_("dashboard.task-card.open-context-menu")}
    />
</div>
