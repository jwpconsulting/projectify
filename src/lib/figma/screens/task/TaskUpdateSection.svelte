<script lang="ts">
    import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    export let action: (() => void) | undefined = undefined;

    $: label = task.workspace_board_section?.title || "missing";
</script>

<SectionLocationState {label} {action} />
