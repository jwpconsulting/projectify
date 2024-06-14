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

    import type { ProjectDetailTask } from "$lib/types/workspace";

    export let task: ProjectDetailTask;
    $: subTaskCompletionPercentage = task.sub_task_progress;
</script>

<div class="flex shrink-0 flex-row items-center gap-2 px-2 py-1">
    {#if subTaskCompletionPercentage !== null}
        <div class="flex flex-row items-center gap-2">
            <div class="flex h-5 w-5 flex-row items-center">
                <Icon src={ViewList} theme="outline" class="text-primary" />
            </div>
            <div class="font-bold text-primary">
                {$number(subTaskCompletionPercentage, {
                    style: "percent",
                })}
            </div>
        </div>
    {/if}
</div>
