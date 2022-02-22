<script lang="ts">
    import { goto } from "$app/navigation";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";

    import Signin from "$lib/components/signin.svelte";
    import { user, singinRedirect } from "$lib/stores/user";

    const rediretURL = "/dashboard";
    if ($user) {
        goto(rediretURL);
    } else {
        singinRedirect.to = rediretURL;
    }
</script>

<PageLayout>
    {#if !$user}
        <main class="page page-center bg-base-200">
            <Signin />
        </main>
    {/if}
</PageLayout>
