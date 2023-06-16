<script lang="ts">
    import { user, userIsLoading } from "$lib/stores/user";
    import Loading from "$lib/components/loading.svelte";
</script>

{#if $user}
    <slot />
{:else if $userIsLoading}
    <main class="page page-center">
        <Loading />
    </main>
{/if}
