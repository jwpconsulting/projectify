<script lang="ts">
    import type { PageData } from "./$types";

    import Members from "$lib/figma/screens/workspace-settings/Members.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard";

    export let data: PageData;

    let { workspace } = data;
    $: workspace = $currentWorkspace ?? workspace;
</script>

<Members {workspace} />
