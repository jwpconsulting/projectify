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
    import { currentProject } from "$lib/stores/dashboard";
    import type { SectionWithTasks } from "$lib/types/workspace";
    import { getProjectSearchUrl } from "$lib/urls/dashboard";

    $: project = $currentProject;
    let searchInput: string | undefined = undefined;

    $: canSearch = searchInput !== undefined;
    $: projectHasTasks =
        project &&
        project.sections.some((s: SectionWithTasks) => s.tasks.length > 0);
</script>

<div class="flex h-full flex-col items-center gap-4 bg-background py-4">
    {#if project && projectHasTasks}
        <form
            action={getProjectSearchUrl(project)}
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
                size="medium"
                color="blue"
                grow={false}
            />
        </form>
    {/if}
    <!-- shared layout for project and search results -->
    <div class="flex w-full grow flex-col">
        <slot />
    </div>
</div>
