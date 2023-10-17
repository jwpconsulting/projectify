<script lang="ts">
    import type { PageData } from "./$types";

    import ReadTaskCard from "$lib/figma/screens/task/ReadTaskCard.svelte";

    export let data: PageData;

    const { task } = data;
</script>

<ReadTaskCard {task} />
