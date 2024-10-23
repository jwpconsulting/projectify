<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
<script lang="ts">
    export let title: string;
    export let action: () => Promise<void>;

    // TODO use undefined
    export let subTitle: string | null = null;
</script>

<!-- TODO this could use more padding -->
<form class="flex flex-col gap-12 p-3" on:submit|preventDefault={action}>
    <h1 class="text-center text-4xl font-bold">
        {title}
    </h1>
    {#if subTitle}
        <h2 class="text-center">
            {subTitle}
        </h2>
    {/if}
    <slot />
</form>
