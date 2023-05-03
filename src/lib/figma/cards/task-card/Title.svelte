<script lang="ts">
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
</script>

<div class="flex flex-row items-center gap-1 sm:gap-6">
    <div class="text-task-update-text text-sm font-bold">
        #{task.number}
    </div>
    <div
        class="line-clamp-2 justify-self-start overflow-hidden text-ellipsis text-left text-sm font-bold text-base-content lg:line-clamp-1"
    >
        {task.title}
    </div>
</div>
