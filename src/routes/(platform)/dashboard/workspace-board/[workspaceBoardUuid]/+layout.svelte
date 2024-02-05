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
    import { Search } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { WorkspaceBoardSectionWithTasks } from "$lib/types/workspace";
    import { getWorkspaceBoardSearchUrl } from "$lib/urls/dashboard";

    import type { LayoutData } from "./$types";

    export let data: LayoutData;

    $: workspaceBoard = data.workspaceBoard;
    let searchInput: string | undefined = undefined;

    $: canSearch = searchInput !== undefined;
    $: workspaceBoardHasTasks = workspaceBoard.workspace_board_sections.some(
        (s: WorkspaceBoardSectionWithTasks) => s.tasks.length > 0,
    );
</script>

<div
    class="flex h-full flex-col items-center gap-4 overflow-y-auto bg-background py-4"
>
    {#if workspaceBoardHasTasks}
        <form
            action={getWorkspaceBoardSearchUrl(workspaceBoard)}
            class="flex w-full max-w-md flex-col gap-2 rounded-xl bg-foreground px-4 py-4"
        >
            <!-- XXX definitely not ideal, placeholder will disappear after input -->
            <InputField
                style={{ inputType: "text" }}
                label={$_("dashboard.search-task.input.label")}
                placeholder={$_("dashboard.search-task.input.placeholder")}
                name="search"
                bind:value={searchInput}
                showClearButton={false}
                required
            />
            <Button
                label={$_("dashboard.search-task.button")}
                action={{ kind: "submit", disabled: !canSearch }}
                style={{
                    kind: "tertiary",
                    icon: { position: "left", icon: Search },
                }}
                size="small"
                color="blue"
                grow={false}
            />
        </form>
    {/if}
    <!-- shared layout for workspace board and search results -->
    <!-- XXX: setting overflow-x-auto here magically solves an overflowing task card
    Why? Justus 2023-08-28 -->
    <div class="flex w-full grow flex-col">
        <slot />
    </div>
</div>
