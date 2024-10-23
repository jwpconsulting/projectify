<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";

    import type { PageData } from "./$types";

    export let data: PageData;

    $: workspace = $currentWorkspace.or(data.workspace);
</script>

<svelte:head>
    <title>{workspace.title}</title>
</svelte:head>

<div class="flex h-full flex-col items-center bg-background px-0 py-8 sm:px-2">
    <slot />
</div>
