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
    import { ViewList } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { number } from "svelte-i18n";

    import type { Task } from "$lib/types/workspace";
    import { getSubTaskProgress } from "$lib/utils/workspace";

    export let task: Task;
    let subTaskCompletionPercentage: number | undefined = undefined;
    $: subTaskCompletionPercentage = task.sub_tasks
        ? getSubTaskProgress(task.sub_tasks)
        : undefined;
</script>

<div class="flex shrink-0 flex-row items-center gap-2 px-2 py-1">
    {#if subTaskCompletionPercentage !== undefined}
        <div class="flex flex-row items-center gap-2">
            <div class="flex h-5 w-5 flex-row items-center">
                <Icon src={ViewList} theme="outline" class="text-primary" />
            </div>
            <div class="text-sm font-bold text-primary">
                {$number(subTaskCompletionPercentage, {
                    style: "percent",
                })}
            </div>
        </div>
    {/if}
</div>
