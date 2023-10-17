<script lang="ts">
    import type { PageData } from "./$types";

    import UpdateTaskCard from "$lib/figma/screens/task/UpdateTaskCard.svelte";

    export let data: PageData;
    const { task } = data;
</script>

<UpdateTaskCard {task} />
