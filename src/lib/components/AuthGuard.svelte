<script lang="ts">
    import { user, userIsLoading } from "$lib/stores/user";
    import Signin from "$lib/components/signin.svelte";
    import Loading from "$lib/components/loading.svelte";
</script>

{#if $user}
    <slot />
{:else if $userIsLoading}
    <main class="page page-center">
        <Loading />
    </main>
{:else}
    <main class="page page-center">
        <Signin />
    </main>
{/if}
