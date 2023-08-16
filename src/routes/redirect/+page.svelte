<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$lib/navigation";

    onMount(async () => {
        if (location.pathname != "/") {
            goto(location.pathname);
        }
    });
</script>
