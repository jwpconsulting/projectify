<script lang="ts">
    import { goto } from "$app/navigation";

    import Signin from "$lib/components/signin.svelte";
    import { user, singinRedirect } from "$lib/stores/user";

    const rediretURL = "/dashboard";
    if ($user) {
        goto(rediretURL);
    } else {
        console.log("aaa");

        singinRedirect.to = rediretURL;
    }
</script>

{#if !$user}
    <main class="page page-center">
        <Signin />
    </main>
{/if}
