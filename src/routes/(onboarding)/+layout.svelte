<script>
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import { user } from "$lib/stores/user";
</script>

<div class="flex grow flex-col overflow-y-auto">
    {#if $user}
        <HeaderDashboard user={$user} />
    {/if}
    <slot />
</div>

<ConnectionStatus />
<ContextMenuContainer />
