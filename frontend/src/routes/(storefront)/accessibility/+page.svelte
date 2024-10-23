<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";
    import { toMarkdown } from "$lib/utils/markdown";

    import HeroAccessibility from "./hero-accessibility.png?enhanced";

    $: heroContent = {
        title: $_("accessibility.hero.title"),
        image: {
            src: HeroAccessibility,
            alt: $_("accessibility.hero.illustration.alt"),
        },
    } satisfies SolutionsHeroContent;

    $: markdown = toMarkdown($_("accessibility.content"));
</script>

<svelte:head>
    <title>{$_("accessibility.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <Hero slot="hero" {heroContent} />

    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
    <main class="prose" slot="content">{@html markdown.content}</main>
</HeroLayout>
