<script lang="ts">
    import { goto } from "$app/navigation";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";

    import Signin from "$lib/components/signin.svelte";
    import { user, signinRedirect } from "$lib/stores/user";

    const redirectUrl = "/dashboard";
    if ($user) {
        goto(redirectUrl);
    } else {
        signinRedirect.to = redirectUrl;
    }
</script>

<PageLayout>
    {#if !$user}
        <main class="page page-center bg-base-200">
            <Signin />
        </main>
    {/if}
</PageLayout>
