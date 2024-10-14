<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import { toMarkdown } from "$lib/utils/markdown";

    $: markdown = toMarkdown($_("free-software.content"));
</script>

<svelte:head>
    <title>{$_("free-software.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <div slot="hero">
        <h1 class="text-3xl font-bold">{$_("free-software.hero")}</h1>
    </div>
    <div slot="content" class="prose">
        <p>{$_("free-software.header")}</p>
        <!-- make sure to add future authors here -->
        <ul>
            <li>Copyright 2021-2024 JWP Consulting GK</li>
        </ul>
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html markdown.content}
    </div>
</HeroLayout>
