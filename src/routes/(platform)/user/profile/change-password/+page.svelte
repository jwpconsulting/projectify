<script lang="ts">
    import type { PageData } from "./$types";

    import Page from "$lib/figma/screens/user-account-settings/Page.svelte";

    export let data: PageData;
    let { user } = data;
</script>

<Page bind:user mode="change-password" />
