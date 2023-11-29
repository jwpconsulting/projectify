<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { getTaskPosition, moveUp, moveDown } from "$lib/stores/modules";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;

    let isFirst = false;
    let isLast = false;
    $: {
        const position = getTaskPosition(workspaceBoardSection, task);
        isFirst = position.kind === "start";
        isLast = position.kind === "end";
    }
</script>

<div class="flex flex-row items-center gap-1">
    <CircleIcon
        size="medium"
        icon="up"
        action={{
            kind: "button",
            action: () => moveUp(workspaceBoardSection, task, { fetch }),
            disabled: isFirst,
        }}
    />
    <CircleIcon
        size="medium"
        icon="down"
        action={{
            kind: "button",
            action: () => moveDown(workspaceBoardSection, task, { fetch }),
            disabled: isLast,
        }}
    />
</div>
