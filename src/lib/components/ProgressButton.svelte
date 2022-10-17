<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ViewList } from "@steeze-ui/heroicons";
    import type { Task } from "$lib/types/workspace";
    export let task: Task;
    let subTaskCompletionPercentage: number | null = null;

    if (task.sub_tasks) {
        const completed = task.sub_tasks.filter(
            (subTask) => subTask.done === true
        ).length;
        const total = task.sub_tasks.length;
        if (completed == total) {
            subTaskCompletionPercentage = 100;
        } else {
            subTaskCompletionPercentage = (completed / total) * 100;
        }
    }
</script>

<div class="flex shrink-0 flex-row items-center gap-2 px-2 py-1">
    <div class="flex flex-row items-center gap-2">
        <div class="flex h-5 w-5 flex-row items-center">
            <Icon src={ViewList} theme="outline" class="text-primary" />
        </div>
        <div class="text-sm font-bold text-primary">
            {subTaskCompletionPercentage} %
        </div>
    </div>
</div>
