<script lang="ts">
    import { user, userIsLoading } from "$lib/stores/user";
    import Signin from "$lib/components/signin.svelte";
    import { _ } from "svelte-i18n";
    import PageLayout from "./layouts/pageLayout.svelte";
</script>

{#if $user}
    <slot />
{:else if $userIsLoading}
    <main class="page page-center">{$_("loading")}</main>
{:else}
    <PageLayout>
        <main class="page page-center bg-base-200">
            <Signin />
        </main>
    </PageLayout>
{/if}
