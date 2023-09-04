<script lang="ts">
    import type { PageData } from "./$types";

    import Billing from "$lib/figma/screens/workspace-settings/Billing.svelte";

    export let data: PageData;

    let { workspace, customer } = data;
</script>

<Billing {customer} {workspace} />
