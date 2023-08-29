<script lang="ts">
    import SectionLocationState from "$lib/figma/screens/task/SectionLocationState.svelte";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    export let workspaceBoardSection: WorkspaceBoardSection;
    export let action: (() => void) | undefined = undefined;
</script>

<SectionLocationState label={workspaceBoardSection.title} {action} />
