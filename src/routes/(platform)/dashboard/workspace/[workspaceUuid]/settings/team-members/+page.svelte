<script lang="ts">
    import type { PageData } from "./$types";

    import Members from "$lib/figma/screens/workspace-settings/Members.svelte";

    export let data: PageData;

    const { workspace } = data;
</script>

<Members {workspace} />
