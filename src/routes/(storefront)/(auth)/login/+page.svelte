<script lang="ts">
    import type { PageData } from "./$types";

    import LogIn from "$lib/figma/screens/auth/LogIn.svelte";

    export let data: PageData;
    const { redirectTo } = data;
</script>

<LogIn {redirectTo} />
