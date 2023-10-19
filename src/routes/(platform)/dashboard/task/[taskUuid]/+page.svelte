<script lang="ts">
    import ReadTaskCard from "$lib/figma/screens/task/ReadTaskCard.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { task } = data;
</script>

<ReadTaskCard {task} />
