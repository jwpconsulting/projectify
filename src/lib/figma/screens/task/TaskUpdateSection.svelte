<script lang="ts">
    import type { Task } from "$lib/types/workspace";
    import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";

    export let task: Task;
    export let action: (() => void) | undefined = undefined;

    $: label = task.workspace_board_section?.title || "missing";
</script>

<div class="flex flex-row items-center gap-5">
    <SectionLocationState {label} {action} />
</div>
