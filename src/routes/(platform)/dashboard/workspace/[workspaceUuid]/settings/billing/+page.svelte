<script lang="ts">
    import type { PageData } from "./$types";

    import WorkspaceSettingsBilling from "$lib/figma/screens/workspace-settings/WorkspaceSettingsBilling.svelte";

    export let data: PageData;

    let { workspace, customer } = data;
</script>

<WorkspaceSettingsBilling {customer} {workspace} />
