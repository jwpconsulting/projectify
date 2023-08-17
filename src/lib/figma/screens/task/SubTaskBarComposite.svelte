<script lang="ts">
    import SubTaskC from "$lib/figma/buttons/SubTask.svelte";
    import SubTaskBar from "$lib/figma/screens/task/SubTaskBar.svelte";
    import type { SubTask } from "$lib/types/workspace";

    export let subTasks: SubTask[];

    // TODO calculate progress
    const progress = 50;
    // TODO determine correct state for children. Or should they do that
    // themselves?
</script>

<SubTaskBar {progress} />
<div class="flex flex-col">
    {#each subTasks as update}
        <SubTaskC
            createOrUpdateSubTask={{ kind: "update", update }}
            state="normal"
        />
    {/each}
</div>
