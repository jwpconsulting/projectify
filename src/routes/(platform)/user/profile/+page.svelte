<script lang="ts">
    import Overview from "$lib/figma/screens/user-account-settings/Overview.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { user } = data;
</script>

<Overview {user} />
