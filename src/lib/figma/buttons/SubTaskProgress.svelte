<script lang="ts">
    import { ViewList } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { number } from "svelte-i18n";

    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    let subTaskCompletionPercentage: number | undefined = undefined;

    $: {
        if (task.sub_tasks !== undefined && task.sub_tasks.length > 0) {
            const completed = task.sub_tasks.filter(
                (subTask) => subTask.done
            ).length;
            const total = task.sub_tasks.length;
            if (completed == total) {
                subTaskCompletionPercentage = 1;
            } else {
                subTaskCompletionPercentage = completed / total;
            }
        } else {
            subTaskCompletionPercentage = undefined;
        }
    }
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
