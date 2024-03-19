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

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { Task } from "$lib/types/workspace";
    import { getTaskUrl } from "$lib/urls";

    export let task: Task;
</script>

<div
    class="flex flex-row items-start items-center gap-1 self-start sm:gap-6 lg:self-center"
>
    <div class="shrink-0">
        <Anchor
            label={$_("dashboard.task-card.task-number", {
                values: { number: task.number },
            })}
            href={getTaskUrl(task.uuid)}
            size="normal"
        />
    </div>
    <div class="line-clamp-3 justify-self-start lg:line-clamp-1 lg:h-6">
        <Anchor
            label={task.title}
            href={getTaskUrl(task.uuid)}
            size="normal"
        />
    </div>
</div>
