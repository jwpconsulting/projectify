<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import { toMarkdown } from "$lib/utils/markdown";

    $: markdown = toMarkdown($_("security.general.content"));
</script>

<svelte:head>
    <title>{$_("security.general.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
    <main class="prose" slot="content">{@html markdown.content}</main>
</HeroLayout>
