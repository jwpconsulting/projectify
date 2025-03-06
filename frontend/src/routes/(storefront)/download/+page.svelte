<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2025 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";

    import { toMarkdown } from "$lib/utils/markdown";

    $: markdown = toMarkdown($_("download.content"));
</script>

<svelte:head>
    <title>{$_("download.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <div slot="hero">
        <h1 class="text-3xl font-bold">{$_("download.header")}</h1>
    </div>

    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
    <main class="prose" slot="content">{@html markdown.content}</main>
</HeroLayout>
