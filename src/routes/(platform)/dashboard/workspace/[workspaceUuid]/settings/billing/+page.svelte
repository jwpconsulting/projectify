<script lang="ts">
    import Billing from "$lib/figma/screens/workspace-settings/Billing.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { customer } = data;
</script>

<Billing {customer} />
