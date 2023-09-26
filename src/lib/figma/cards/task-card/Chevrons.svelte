<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { getTaskPosition, moveUp, moveDown } from "$lib/stores/modules";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;

    $: isFirst = workspaceBoardSection
        ? getTaskPosition(workspaceBoardSection, task) === "start"
        : false;
    $: isLast = workspaceBoardSection
        ? getTaskPosition(workspaceBoardSection, task) === "end"
        : false;
</script>

<div class="flex flex-row items-center gap-1">
    <CircleIcon
        size="medium"
        icon="up"
        action={{
            kind: "button",
            action: () => moveUp(workspaceBoardSection, task),
            disabled: isFirst,
        }}
    />
    <CircleIcon
        size="medium"
        icon="down"
        action={{
            kind: "button",
            action: () => moveDown(workspaceBoardSection, task),
            disabled: isLast,
        }}
    />
</div>
