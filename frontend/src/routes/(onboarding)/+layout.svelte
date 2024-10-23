<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import { currentUser } from "$lib/stores/user";
</script>

<div class="flex grow flex-col overflow-y-auto">
    {#if $currentUser.kind === "authenticated"}
        <HeaderDashboard user={$currentUser} />
    {/if}
    <slot />
</div>

<ConnectionStatus />
<ContextMenuContainer />
