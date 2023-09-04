<script lang="ts">
    import type { PageData } from "./$types";

    import ReadTaskCard from "$lib/figma/screens/task/ReadTaskCard.svelte";

    export let data: PageData;

    let { task, workspaceBoardSection } = data;
</script>

<ReadTaskCard {task} {workspaceBoardSection} />
