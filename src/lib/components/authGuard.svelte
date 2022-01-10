<script lang="ts">
    import { user } from "$lib/stores/user";
    import Signin from "$lib/components/signin.svelte";
</script>

{#if $user}
    <slot />
{:else}
    <main class="page page-center">
        <Signin />
    </main>
{/if}
