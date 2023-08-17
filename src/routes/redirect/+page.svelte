<script lang="ts">
    import { onMount } from "svelte";

    import { goto } from "$lib/navigation";

    // XXX safe to get rid of this page? Justus 2023-08-17
    onMount(async () => {
        if (location.pathname != "/") {
            await goto(location.pathname);
        }
    });
</script>
