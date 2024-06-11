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
<!-- TODO At some point we will add the tab bar and bread crumbs here -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import { currentTask } from "$lib/stores/dashboard/task";

    import type { LayoutData } from "./$types";

    export let data: LayoutData;

    $: task = $currentTask.orPromise(data.task);
</script>

<svelte:head>
    {#await task}
        <title>{$_("task.title-loading")}</title>
    {:then task}
        <title>
            {$_("task.title", { values: { title: task.title } })}
        </title>
    {/await}
</svelte:head>

<slot />
