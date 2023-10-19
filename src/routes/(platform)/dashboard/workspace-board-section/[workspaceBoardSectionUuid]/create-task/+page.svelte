<script lang="ts">
    import CreateTaskCard from "$lib/figma/screens/task/CreateTaskCard.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { workspaceBoardSection } = data;
</script>

<CreateTaskCard {workspaceBoardSection} />
