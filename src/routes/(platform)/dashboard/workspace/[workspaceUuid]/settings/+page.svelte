<script lang="ts">
    import General from "$lib/figma/screens/workspace-settings/General.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { workspace } = data;
</script>

<General {workspace} />
