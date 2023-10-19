<script lang="ts">
    import UpdateTaskCard from "$lib/figma/screens/task/UpdateTaskCard.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { task } = data;
</script>

<UpdateTaskCard {task} />
