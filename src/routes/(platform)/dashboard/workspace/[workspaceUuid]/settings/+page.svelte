<script lang="ts">
    import type { PageData } from "./$types";

    import WorkspaceSettingsGeneral from "$lib/figma/screens/workspace-settings/WorkspaceSettingsGeneral.svelte";

    export let data: PageData;

    let { workspace } = data;
</script>

<WorkspaceSettingsGeneral {workspace} />
