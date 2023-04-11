<script lang="ts">
    import AuthGuard from "$lib/components/AuthGuard.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";

    import { user } from "$lib/stores/user";
</script>

<AuthGuard>
    <div class="flex h-screen flex-col">
        {#if $user}
            <HeaderDashboard user={$user} />
        {/if}
        <slot />
    </div>
</AuthGuard>
