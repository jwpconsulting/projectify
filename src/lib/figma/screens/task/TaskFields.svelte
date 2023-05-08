<script lang="ts">
    import type { Task } from "$lib/types/workspace";
    import { getTaskEditUrl } from "$lib/urls";

    export let task: Task;
</script>

<a href={getTaskEditUrl(task.uuid)}>Edit task</a>

title: {task.title}
