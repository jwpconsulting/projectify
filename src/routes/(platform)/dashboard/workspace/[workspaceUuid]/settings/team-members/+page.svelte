<script lang="ts">
    import type { PageData } from "./$types";

    import WorkspaceSettingsMembers from "$lib/figma/screens/workspace-settings/WorkspaceSettingsMembers.svelte";

    export let data: PageData;

    let { workspace } = data;
</script>

<WorkspaceSettingsMembers {workspace} />
