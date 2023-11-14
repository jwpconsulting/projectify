<script lang="ts">
    import LogIn from "$lib/figma/screens/auth/LogIn.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { redirectTo } = data;
</script>

<LogIn {redirectTo} />
