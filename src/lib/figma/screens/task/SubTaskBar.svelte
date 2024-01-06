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
    import { Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import type { SubTaskAssignment } from "$lib/types/stores";

    export let progress: number | undefined;
    export let subTaskAssignment: SubTaskAssignment | undefined = undefined;
    // TODO make buttons do something
    // TODO: Support onInteract
</script>

<div class="flex flex-col gap-4">
    <div class="flex flex-row items-center justify-between">
        <div class="flex flex-row items-center gap-4">
            <!-- no idea if h4 is correct here XXX -->
            <h4 class="text-xl font-bold">
                {$_("task-screen.sub-tasks.title")}
            </h4>
            <!-- TODO: and if there is no progress, display: This task has no sub tasks -->
        </div>
        {#if subTaskAssignment}
            <div class="flex flex-row items-center gap-6">
                <Button
                    style={{
                        kind: "tertiary",
                        icon: { position: "left", icon: Plus },
                    }}
                    color="blue"
                    size="medium"
                    label={$_("task-screen.sub-tasks.add-sub-task.button")}
                    action={{
                        kind: "button",
                        action: subTaskAssignment.addSubTask,
                    }}
                />
            </div>
        {/if}
    </div>
    {#if progress !== undefined}
        <div class="flex flex-row items-center gap-4">
            <div class="h-2 w-full overflow-hidden rounded bg-disabled">
                <div
                    class="h-full bg-primary"
                    style:width="{progress * 100}%"
                />
            </div>
            <p class="min-w-max font-bold">
                {$_("task-screen.sub-tasks.completion", {
                    values: { progress },
                })}
            </p>
        </div>
    {/if}
</div>
