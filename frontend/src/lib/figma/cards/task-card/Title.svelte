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
    import { _ } from "svelte-i18n";

    import type { Task } from "$lib/types/workspace";

    export let task: Task;
</script>

<div class="flex flex-row items-start gap-1 sm:gap-6">
    <div class="text-task-update-text shrink-0 text-sm font-bold">
        {$_("dashboard.task-card.task-number", {
            values: { number: task.number },
        })}
    </div>
    <div
        class="line-clamp-2 h-10 justify-self-start overflow-hidden text-ellipsis text-left text-sm font-bold text-base-content lg:line-clamp-1 lg:h-5"
    >
        {task.title}
    </div>
</div>
