<!--
@component
Up and down chevrons for task movement within a workspace board section
-->
<script lang="ts">
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { getTaskPosition, moveUp, moveDown } from "$lib/stores/modules";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;

    let upDisabled = true;
    let downDisabled = true;
    $: {
        const position = getTaskPosition(workspaceBoardSection, task);
        upDisabled = position.kind === "start";
        // If we are the only task, we don't want to show the down chevron.
        downDisabled =
            position.kind === "start"
                ? position.isOnly
                : position.kind === "end";
    }
</script>

<div class="flex flex-row items-center gap-1">
    <CircleIcon
        size="medium"
        icon="up"
        action={{
            kind: "button",
            action: () => moveUp(workspaceBoardSection, task, { fetch }),
            disabled: upDisabled,
        }}
    />
    <CircleIcon
        size="medium"
        icon="down"
        action={{
            kind: "button",
            action: () => moveDown(workspaceBoardSection, task, { fetch }),
            disabled: downDisabled,
        }}
    />
</div>
