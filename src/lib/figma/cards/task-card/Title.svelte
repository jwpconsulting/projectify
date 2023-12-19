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
