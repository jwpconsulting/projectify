<script lang="ts">
    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
    onMount(async () => {
        if (location.pathname != "/") {
            goto(location.pathname);
        }
    });
</script>

<main class="page page-center">
    <h1>HOME</h1>
</main>
