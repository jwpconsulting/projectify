<script lang="ts">
    import type { Task } from "$lib/types";
    export let task: Task;
</script>

<div class="flex flex-row items-center gap-1 sm:gap-6">
    <div class="text-task-update-text text-sm font-bold">
        #{task.number}
    </div>
    <div
        class="justify-self-start overflow-hidden text-ellipsis text-left text-sm font-bold text-base-content line-clamp-2 lg:line-clamp-1"
    >
        {task.title}
    </div>
</div>
