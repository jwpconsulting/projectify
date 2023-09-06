<script lang="ts">
    import type { PageData } from "./$types";

    import General from "$lib/figma/screens/workspace-settings/General.svelte";

    export let data: PageData;

    const { workspace } = data;
</script>

<General {workspace} />
