<script lang="ts">
    import { user, userIsLoading } from "$lib/stores/user";
    import Signin from "$lib/components/signin.svelte";
    import { _ } from "svelte-i18n";
</script>

{#if $user}
    <slot />
{:else if $userIsLoading}
    <main class="page page-center">{$_("loading")}</main>
{:else}
    <main class="page page-center">
        <Signin />
    </main>
{/if}
