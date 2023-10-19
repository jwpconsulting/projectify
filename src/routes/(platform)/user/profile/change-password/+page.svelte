<script lang="ts">
    import Page from "$lib/figma/screens/user-account-settings/Page.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    let { user } = data;
</script>

<Page bind:user mode="change-password" />
