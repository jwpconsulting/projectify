<script lang="ts">
    import type { PageData } from "./$types";

    import CreateTaskCard from "$lib/figma/screens/task/CreateTaskCard.svelte";

    export let data: PageData;

    const { workspaceBoardSection } = data;
</script>

<CreateTaskCard {workspaceBoardSection} />
