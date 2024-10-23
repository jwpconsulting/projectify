<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";
</script>

<svelte:head>
    <title>{$_("user-account-settings.title")}</title>
</svelte:head>

<div class="flex h-full flex-col items-center bg-background p-8">
    <div class="w-full max-w-lg">
        <div class="flex flex-col gap-4">
            <h1 class="text-2xl font-bold">
                {$_("user-account-settings.title")}
            </h1>
            <div class="flex flex-col gap-12 rounded-lg bg-foreground p-4">
                <slot />
            </div>
        </div>
    </div>
</div>
