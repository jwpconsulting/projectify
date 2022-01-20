<script lang="ts">
    import { goto } from "$app/navigation";

    import Signin from "$lib/components/signin.svelte";
    import { user } from "$lib/stores/user";

    $: {
        if ($user) {
            goto("/dashboard");
        }
    }
</script>

<main class="page page-center">
    <Signin />
</main>
