<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { ChevronDown, ChevronRight, Plus } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { toggleWorkspaceBoardSectionOpen } from "$lib/stores/dashboard";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import { getNewTaskUrl } from "$lib/urls";

    export let workspaceBoard: WorkspaceBoard;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let open: boolean;

    const { uuid } = workspaceBoardSection;
    $: toggleOpen = toggleWorkspaceBoardSectionOpen.bind(null, uuid);
    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        const contextMenuType: ContextMenuType = {
            kind: "workspaceBoardSection",
            workspaceBoard,
            workspaceBoardSection,
        };
        await openContextMenu(contextMenuType, dropDownMenuBtnRef);
    }
</script>

<header
    class="flex w-full flex-row items-center justify-between bg-foreground px-4 py-2"
>
    <div
        data-figma-name="Section header"
        class="flex min-w-0 shrink flex-row gap-4 text-base-content"
    >
        <button on:click={toggleOpen}>
            <Icon
                src={open ? ChevronDown : ChevronRight}
                class="h-6 w-6"
                theme="outline"
            />
        </button>
        <h1 class="line-clamp-1 min-w-0 shrink font-bold">
            {workspaceBoardSection.title}
        </h1>
    </div>
    <div
        class="flex shrink-0 flex-row items-center gap-1"
        data-figma-name="Right side"
    >
        <Button
            action={{
                kind: "a",
                href: getNewTaskUrl(workspaceBoardSection.uuid),
            }}
            style={{
                kind: "tertiary",
                icon: { position: "left", icon: Plus },
            }}
            size="medium"
            color="blue"
            label={$_("dashboard.section.add-task")}
        />
        <div bind:this={dropDownMenuBtnRef}>
            <SquovalIcon
                icon="ellipsis"
                state="active"
                active={false}
                action={{ kind: "button", action: openDropDownMenu }}
            />
        </div>
    </div>
</header>
