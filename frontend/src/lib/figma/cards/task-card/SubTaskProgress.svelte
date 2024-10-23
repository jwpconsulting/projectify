<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
